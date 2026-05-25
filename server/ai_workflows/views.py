from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    AIAgentProfile,
    AIKnowledgeDocument,
    AIPipelineTemplate,
    AIPipelineRun,
)
from .serializers import (
    AIAgentProfileSerializer,
    AIKnowledgeDocumentSerializer,
    AIPipelineTemplateSerializer,
    AIPipelineRunSerializer,
)
from .tasks import execute_ai_pipeline


class AIAgentProfileViewSet(viewsets.ModelViewSet):
    queryset = AIAgentProfile.objects.all()
    serializer_class = AIAgentProfileSerializer

    def get_queryset(self):
        org_id = self.kwargs.get('org_id')
        if org_id:
            return self.queryset.filter(organization_id=org_id)
        return self.queryset

    def perform_create(self, serializer):
        org_id = self.kwargs.get('org_id')
        serializer.save(organization_id=org_id)


class AIKnowledgeDocumentViewSet(viewsets.ModelViewSet):
    queryset = AIKnowledgeDocument.objects.all()
    serializer_class = AIKnowledgeDocumentSerializer

    def get_queryset(self):
        org_id = self.kwargs.get('org_id')
        if org_id:
            return self.queryset.filter(organization_id=org_id)
        return self.queryset

    def perform_create(self, serializer):
        org_id = self.kwargs.get('org_id')
        serializer.save(organization_id=org_id)


class AIPipelineTemplateViewSet(viewsets.ModelViewSet):
    queryset = AIPipelineTemplate.objects.all()
    serializer_class = AIPipelineTemplateSerializer

    def get_queryset(self):
        org_id = self.kwargs.get('org_id')
        if org_id:
            return self.queryset.filter(organization_id=org_id)
        return self.queryset

    def perform_create(self, serializer):
        org_id = self.kwargs.get('org_id')
        serializer.save(organization_id=org_id)


class AIPipelineRunViewSet(viewsets.ModelViewSet):
    queryset = AIPipelineRun.objects.all()
    serializer_class = AIPipelineRunSerializer

    def get_queryset(self):
        org_id = self.kwargs.get('org_id')
        if org_id:
            return self.queryset.filter(organization_id=org_id)
        return self.queryset

    def perform_create(self, serializer):
        org_id = self.kwargs.get('org_id')
        serializer.save(
            organization_id=org_id,
            triggered_by=self.request.user
        )

    @action(detail=True, methods=['post'])
    def trigger(self, request, org_id=None, pk=None):
        """
        Kicks off the asynchronous multi-agent RAG pipeline execution task in Celery.
        """
        run = self.get_object()
        
        # Verify run belongs to organization
        if str(run.organization_id) != str(org_id):
            return Response(
                {"error": "Run does not match specified organization."},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.core.cache import cache
        lock_key = f"ai_pipeline_trigger_lock_{run.id}"
        
        # 1. Prevent concurrent double-clicks or races using a Redis cache lock
        if not cache.add(lock_key, "locked", timeout=15):
            return Response(
                {"error": "Pipeline execution is already being triggered."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Prevent triggering if the run is already active or finished
        if run.status in ['in_progress', 'completed']:
            return Response(
                {"error": f"Cannot trigger pipeline run in status: {run.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = 'pending'
        run.save(update_fields=['status'])

        # Delay run task in celery
        execute_ai_pipeline.delay(run.id)

        serializer = self.get_serializer(run)
        return Response(serializer.data, status=status.HTTP_200_OK)
