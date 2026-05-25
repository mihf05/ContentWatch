from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.permissions import HasResourcePermission, IsOrgAdmin, IsOrgMember
from .models import Organization, Team, Membership, Invitation, AgencyPartnership
from .serializers import (
    OrganizationSerializer, OrganizationCreateSerializer,
    TeamSerializer, MembershipSerializer,
    InvitationSerializer, InvitationCreateSerializer, InvitationAcceptSerializer,
    AgencyPartnershipSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    CRUD for organizations.
    - List: returns orgs the current user is a member of.
    - Create: any authenticated user can create an org (becomes owner).
    """

    permission_classes = [IsAuthenticated]
    rbac_resource = 'settings'

    def get_queryset(self):
        return Organization.objects.filter(
            memberships__user=self.request.user,
            memberships__is_active=True,
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrganizationCreateSerializer
        return OrganizationSerializer

    def get_permissions(self):
        if self.action in ('create', 'list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasResourcePermission()]


class TeamViewSet(viewsets.ModelViewSet):
    """CRUD for teams within an organization."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = TeamSerializer
    rbac_resource = 'teams'

    def get_queryset(self):
        return Team.objects.filter(organization_id=self.kwargs['org_id'])

    def perform_create(self, serializer):
        serializer.save(organization_id=self.kwargs['org_id'])


class MembershipViewSet(viewsets.ModelViewSet):
    """Manage organization members."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = MembershipSerializer
    rbac_resource = 'teams'
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return Membership.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).select_related('user', 'role', 'team')

    @action(detail=True, methods=['patch'])
    def change_role(self, request, org_id=None, pk=None):
        """Change a member's role."""
        membership = self.get_object()
        role_id = request.data.get('role_id')
        if not role_id:
            return Response(
                {'error': 'role_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        membership.role_id = role_id
        membership.save(update_fields=['role'])
        return Response(MembershipSerializer(membership).data)

    @action(detail=True, methods=['patch'])
    def change_team(self, request, org_id=None, pk=None):
        """Move a member to a different team."""
        membership = self.get_object()
        team_id = request.data.get('team_id')
        membership.team_id = team_id
        membership.save(update_fields=['team'])
        return Response(MembershipSerializer(membership).data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, org_id=None, pk=None):
        """Deactivate a member (soft remove)."""
        membership = self.get_object()
        if membership.organization.owner_id == membership.user_id:
            return Response(
                {'error': 'Cannot deactivate the organization owner'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        membership.is_active = False
        membership.save(update_fields=['is_active'])
        return Response({'status': 'deactivated'})

    @action(detail=True, methods=['post'])
    def reactivate(self, request, org_id=None, pk=None):
        """Reactivate a previously deactivated member."""
        membership = self.get_object()
        membership.is_active = True
        membership.save(update_fields=['is_active'])
        return Response({'status': 'reactivated'})


class InvitationViewSet(viewsets.ModelViewSet):
    """Manage invitations to join an organization."""

    permission_classes = [IsAuthenticated, IsOrgAdmin]
    serializer_class = InvitationSerializer
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        return Invitation.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).select_related('invited_by', 'role', 'team')

    def create(self, request, org_id=None):
        serializer = InvitationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        invitation = Invitation.objects.create(
            organization_id=org_id,
            email=data['email'],
            role_id=data.get('role_id'),
            team_id=data.get('team_id'),
            invited_by=request.user,
            message=data.get('message', ''),
            expires_at=timezone.now() + timezone.timedelta(days=7),
        )
        return Response(
            InvitationSerializer(invitation).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, org_id=None):
        """Accept an invitation by token."""
        serializer = InvitationAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        try:
            invitation = Invitation.objects.get(token=token, status='pending')
        except Invitation.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired invitation'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if invitation.is_expired:
            invitation.status = 'expired'
            invitation.save(update_fields=['status'])
            return Response(
                {'error': 'Invitation has expired'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create membership
        membership, created = Membership.objects.get_or_create(
            user=request.user,
            organization=invitation.organization,
            defaults={
                'role': invitation.role,
                'team': invitation.team,
            },
        )

        if not created:
            # User already a member — reactivate if needed
            membership.is_active = True
            membership.role = invitation.role or membership.role
            membership.team = invitation.team or membership.team
            membership.save()

        invitation.status = 'accepted'
        invitation.save(update_fields=['status'])

        return Response({
            'status': 'accepted',
            'organization': OrganizationSerializer(invitation.organization).data,
        })

    @action(detail=True, methods=['post'])
    def resend(self, request, org_id=None, pk=None):
        """Resend an invitation (refresh expiry)."""
        invitation = self.get_object()
        invitation.expires_at = timezone.now() + timezone.timedelta(days=7)
        invitation.status = 'pending'
        invitation.save(update_fields=['expires_at', 'status'])
        return Response({'status': 'resent'})


class AgencyPartnershipViewSet(viewsets.ModelViewSet):
    """Manage agency-creator/brand partnerships."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = AgencyPartnershipSerializer
    rbac_resource = 'settings'

    def get_queryset(self):
        org_id = self.kwargs['org_id']
        return AgencyPartnership.objects.filter(
            models.Q(agency_id=org_id) | models.Q(partner_id=org_id),
        ).select_related('agency', 'partner')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def accept(self, request, org_id=None, pk=None):
        partnership = self.get_object()
        partnership.status = 'active'
        partnership.started_at = timezone.now().date()
        partnership.save(update_fields=['status', 'started_at'])
        return Response(AgencyPartnershipSerializer(partnership).data)

    @action(detail=True, methods=['post'])
    def terminate(self, request, org_id=None, pk=None):
        partnership = self.get_object()
        partnership.status = 'terminated'
        partnership.ends_at = timezone.now().date()
        partnership.save(update_fields=['status', 'ends_at'])
        return Response(AgencyPartnershipSerializer(partnership).data)


# Need to import models for Q lookup
from django.db import models
