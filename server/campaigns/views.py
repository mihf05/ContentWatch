from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.permissions import HasResourcePermission
from .models import Campaign, CampaignStage, CampaignDeliverable
from .serializers import (
    CampaignSerializer, CampaignListSerializer, CampaignCreateSerializer,
    CampaignStageSerializer, CampaignDeliverableSerializer,
)


class CampaignViewSet(viewsets.ModelViewSet):
    """CRUD for campaigns within an organization."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    rbac_resource = 'campaigns'

    def get_queryset(self):
        qs = Campaign.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).select_related('client', 'created_by', 'workflow')

        # Filters
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        priority = self.request.query_params.get('priority')
        if priority:
            qs = qs.filter(priority=priority)

        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return CampaignListSerializer
        if self.action in ('create',):
            return CampaignCreateSerializer
        return CampaignSerializer

    @action(detail=True, methods=['post'])
    def transition(self, request, org_id=None, pk=None):
        """
        Transition campaign to a new status.
        POST body: {"status": "in_progress"}
        """
        campaign = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = dict(Campaign.STATUS_CHOICES)
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Choose from: {list(valid_statuses.keys())}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        campaign.status = new_status
        campaign.save(update_fields=['status', 'updated_at'])
        return Response(CampaignSerializer(campaign).data)

    @action(detail=True, methods=['get'])
    def timeline(self, request, org_id=None, pk=None):
        """Get campaign timeline with stages and deliverables."""
        campaign = self.get_object()
        stages = campaign.stages.all().order_by('order')
        return Response({
            'campaign': CampaignListSerializer(campaign).data,
            'stages': CampaignStageSerializer(stages, many=True).data,
            'deliverables': CampaignDeliverableSerializer(
                campaign.deliverables.all(), many=True,
            ).data,
        })


class CampaignStageViewSet(viewsets.ModelViewSet):
    """CRUD for stages within a campaign."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = CampaignStageSerializer
    rbac_resource = 'campaigns'

    def get_queryset(self):
        return CampaignStage.objects.filter(
            campaign_id=self.kwargs['campaign_id'],
            campaign__organization_id=self.kwargs['org_id'],
        )

    def perform_create(self, serializer):
        serializer.save(campaign_id=self.kwargs['campaign_id'])

    @action(detail=True, methods=['post'])
    def complete(self, request, org_id=None, campaign_id=None, pk=None):
        stage = self.get_object()
        stage.status = 'completed'
        stage.completed_at = timezone.now()
        stage.save(update_fields=['status', 'completed_at'])
        return Response(CampaignStageSerializer(stage).data)


class CampaignDeliverableViewSet(viewsets.ModelViewSet):
    """CRUD for deliverables within a campaign."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = CampaignDeliverableSerializer
    rbac_resource = 'campaigns'

    def get_queryset(self):
        return CampaignDeliverable.objects.filter(
            campaign_id=self.kwargs['campaign_id'],
            campaign__organization_id=self.kwargs['org_id'],
        )

    def perform_create(self, serializer):
        serializer.save(campaign_id=self.kwargs['campaign_id'])

    @action(detail=True, methods=['post'])
    def transition(self, request, org_id=None, campaign_id=None, pk=None):
        """Transition deliverable status."""
        deliverable = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = dict(CampaignDeliverable.STATUS_CHOICES)
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Choose from: {list(valid_statuses.keys())}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        deliverable.status = new_status
        deliverable.save(update_fields=['status', 'updated_at'])
        return Response(CampaignDeliverableSerializer(deliverable).data)
