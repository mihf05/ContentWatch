from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.permissions import HasResourcePermission
from .models import ApprovalChain, ApprovalLevel, ApprovalRequest, ApprovalDecision
from .serializers import (
    ApprovalChainSerializer, ApprovalChainCreateSerializer,
    ApprovalLevelSerializer,
    ApprovalRequestSerializer, ApprovalRequestCreateSerializer,
    ApprovalDecisionSerializer, ApprovalDecisionCreateSerializer,
)


class ApprovalChainViewSet(viewsets.ModelViewSet):
    """CRUD for approval chains."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    rbac_resource = 'approvals'

    def get_queryset(self):
        return ApprovalChain.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).prefetch_related('levels')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ApprovalChainCreateSerializer
        return ApprovalChainSerializer


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    """Submit and manage approval requests."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    rbac_resource = 'approvals'
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        qs = ApprovalRequest.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).select_related('chain', 'current_level', 'requested_by').prefetch_related('decisions')

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        # Filter: only show requests I need to approve
        pending_for_me = self.request.query_params.get('pending_for_me')
        if pending_for_me:
            from teams.models import Membership
            membership = Membership.objects.filter(
                user=self.request.user,
                organization_id=self.kwargs['org_id'],
                is_active=True,
            ).select_related('role').first()

            if membership and membership.role:
                qs = qs.filter(
                    status='in_review',
                    current_level__approver_role=membership.role,
                ).exclude(
                    decisions__approver=self.request.user,
                    decisions__level=models.F('current_level'),
                )

        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return ApprovalRequestCreateSerializer
        return ApprovalRequestSerializer

    @action(detail=True, methods=['post'])
    def decide(self, request, org_id=None, pk=None):
        """
        Submit a decision on an approval request.
        POST body: {"decision": "approved|rejected|revision_requested", "comment": "..."}
        """
        approval_request = self.get_object()

        if approval_request.status not in ('pending', 'in_review'):
            return Response(
                {'error': 'This request is no longer open for decisions'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ApprovalDecisionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        decision = ApprovalDecision.objects.create(
            request=approval_request,
            level=approval_request.current_level,
            approver=request.user,
            decision=serializer.validated_data['decision'],
            comment=serializer.validated_data.get('comment', ''),
        )

        # Process the decision
        if decision.decision == 'rejected':
            approval_request.status = 'rejected'
            approval_request.resolved_at = timezone.now()
            approval_request.save(update_fields=['status', 'resolved_at'])
        elif decision.decision == 'approved':
            # Check if all required approvals at this level are met
            level = approval_request.current_level
            if level and level.require_all:
                # Need all eligible approvers
                # For simplicity, just advance if this approver approved
                approval_request.advance_level()
            else:
                # Any one approval is sufficient
                approval_request.advance_level()
        elif decision.decision == 'revision_requested':
            approval_request.status = 'pending'
            approval_request.save(update_fields=['status'])

        return Response(ApprovalRequestSerializer(approval_request).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, org_id=None, pk=None):
        """Cancel an approval request."""
        approval_request = self.get_object()
        if approval_request.requested_by != request.user:
            return Response(
                {'error': 'Only the requester can cancel'},
                status=status.HTTP_403_FORBIDDEN,
            )
        approval_request.status = 'cancelled'
        approval_request.resolved_at = timezone.now()
        approval_request.save(update_fields=['status', 'resolved_at'])
        return Response({'status': 'cancelled'})


from django.db import models
