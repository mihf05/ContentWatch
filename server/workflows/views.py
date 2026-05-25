from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.permissions import HasResourcePermission
from .models import WorkflowTemplate, WorkflowStep, WorkflowInstance, StepExecution
from .serializers import (
    WorkflowTemplateSerializer, WorkflowTemplateCreateSerializer,
    WorkflowStepSerializer,
    WorkflowInstanceSerializer, WorkflowInstanceCreateSerializer,
    StepExecutionSerializer,
)


class WorkflowTemplateViewSet(viewsets.ModelViewSet):
    """CRUD for workflow templates."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    rbac_resource = 'workflows'

    def get_queryset(self):
        return WorkflowTemplate.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).prefetch_related('steps')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return WorkflowTemplateCreateSerializer
        return WorkflowTemplateSerializer


class WorkflowStepViewSet(viewsets.ModelViewSet):
    """CRUD for steps within a workflow template."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = WorkflowStepSerializer
    rbac_resource = 'workflows'

    def get_queryset(self):
        return WorkflowStep.objects.filter(
            template_id=self.kwargs['template_id'],
            template__organization_id=self.kwargs['org_id'],
        )

    def perform_create(self, serializer):
        serializer.save(template_id=self.kwargs['template_id'])

    @action(detail=False, methods=['post'])
    def reorder(self, request, org_id=None, template_id=None):
        """
        Reorder steps. Body: {"step_ids": [3, 1, 2]}
        """
        step_ids = request.data.get('step_ids', [])
        for idx, step_id in enumerate(step_ids, start=1):
            WorkflowStep.objects.filter(
                id=step_id,
                template_id=template_id,
            ).update(order=idx)
        return Response({'status': 'reordered'})


class WorkflowInstanceViewSet(viewsets.ModelViewSet):
    """Manage running workflow instances."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    rbac_resource = 'workflows'

    def get_queryset(self):
        return WorkflowInstance.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).select_related('template', 'current_step').prefetch_related('executions')

    def get_serializer_class(self):
        if self.action == 'create':
            return WorkflowInstanceCreateSerializer
        return WorkflowInstanceSerializer

    @action(detail=True, methods=['post'])
    def advance(self, request, org_id=None, pk=None):
        """Advance the workflow to the next step."""
        instance = self.get_object()
        if instance.status != 'active':
            return Response(
                {'error': 'Can only advance active workflows'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark current step execution as completed
        if instance.current_step:
            StepExecution.objects.filter(
                instance=instance,
                step=instance.current_step,
            ).update(status='completed', completed_at=timezone.now())

        has_next = instance.advance()
        return Response(WorkflowInstanceSerializer(instance).data)

    @action(detail=True, methods=['post'])
    def pause(self, request, org_id=None, pk=None):
        instance = self.get_object()
        instance.status = 'paused'
        instance.save(update_fields=['status'])
        return Response({'status': 'paused'})

    @action(detail=True, methods=['post'])
    def resume(self, request, org_id=None, pk=None):
        instance = self.get_object()
        instance.status = 'active'
        instance.save(update_fields=['status'])
        return Response({'status': 'resumed'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, org_id=None, pk=None):
        instance = self.get_object()
        instance.status = 'cancelled'
        instance.completed_at = timezone.now()
        instance.save(update_fields=['status', 'completed_at'])
        return Response({'status': 'cancelled'})


class StepExecutionViewSet(viewsets.ModelViewSet):
    """Manage step executions within a workflow instance."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = StepExecutionSerializer
    rbac_resource = 'workflows'
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        return StepExecution.objects.filter(
            instance_id=self.kwargs['instance_id'],
            instance__organization_id=self.kwargs['org_id'],
        ).select_related('step', 'assigned_to')

    @action(detail=True, methods=['post'])
    def start(self, request, org_id=None, instance_id=None, pk=None):
        execution = self.get_object()
        execution.status = 'in_progress'
        execution.started_at = timezone.now()
        execution.assigned_to = request.user
        execution.save(update_fields=['status', 'started_at', 'assigned_to'])
        return Response(StepExecutionSerializer(execution).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, org_id=None, instance_id=None, pk=None):
        execution = self.get_object()
        execution.status = 'completed'
        execution.completed_at = timezone.now()
        execution.notes = request.data.get('notes', execution.notes)
        execution.save(update_fields=['status', 'completed_at', 'notes'])

        # Auto-advance if configured
        if execution.step.auto_advance:
            execution.instance.advance()

        return Response(StepExecutionSerializer(execution).data)
