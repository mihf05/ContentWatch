from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.permissions import HasResourcePermission, IsOrgMember
from .models import Activity, Comment, Notification, Presence
from .serializers import (
    ActivitySerializer, CommentSerializer, CommentCreateSerializer,
    NotificationSerializer, PresenceSerializer,
)


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only activity feed for an organization."""

    permission_classes = [IsAuthenticated, IsOrgMember]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        qs = Activity.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).select_related('actor')

        # Filters
        resource_type = self.request.query_params.get('resource_type')
        if resource_type:
            qs = qs.filter(resource_type=resource_type)

        resource_id = self.request.query_params.get('resource_id')
        if resource_id:
            qs = qs.filter(resource_id=resource_id)

        action_filter = self.request.query_params.get('action')
        if action_filter:
            qs = qs.filter(action=action_filter)

        return qs[:100]  # Cap at 100 most recent


class CommentViewSet(viewsets.ModelViewSet):
    """Generic comments on any resource."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    rbac_resource = 'collaboration'

    def get_queryset(self):
        qs = Comment.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).select_related('author')

        resource_type = self.request.query_params.get('resource_type')
        resource_id = self.request.query_params.get('resource_id')
        if resource_type and resource_id:
            qs = qs.filter(resource_type=resource_type, resource_id=resource_id)

        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            organization_id=self.kwargs['org_id'],
            author=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.save(is_edited=True)

    @action(detail=True, methods=['post'])
    def pin(self, request, org_id=None, pk=None):
        comment = self.get_object()
        comment.is_pinned = not comment.is_pinned
        comment.save(update_fields=['is_pinned'])
        return Response({'is_pinned': comment.is_pinned})


class NotificationViewSet(viewsets.ModelViewSet):
    """User notifications."""

    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        qs = Notification.objects.filter(
            recipient=self.request.user,
        ).select_related('actor')

        org_id = self.request.query_params.get('org_id')
        if org_id:
            qs = qs.filter(organization_id=org_id)

        unread_only = self.request.query_params.get('unread')
        if unread_only:
            qs = qs.filter(is_read=False)

        return qs

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=['is_read', 'read_at'])
        return Response({'status': 'read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        org_id = request.data.get('org_id')
        qs = Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        )
        if org_id:
            qs = qs.filter(organization_id=org_id)
        count = qs.update(is_read=True, read_at=timezone.now())
        return Response({'marked_read': count})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        org_id = request.query_params.get('org_id')
        qs = Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        )
        if org_id:
            qs = qs.filter(organization_id=org_id)
        return Response({'count': qs.count()})


class PresenceViewSet(viewsets.ModelViewSet):
    """Online presence tracking."""

    permission_classes = [IsAuthenticated, IsOrgMember]
    serializer_class = PresenceSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        # Show all online members in the org
        return Presence.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).exclude(status='offline').select_related('user')

    @action(detail=False, methods=['post'])
    def heartbeat(self, request, org_id=None):
        """Update presence status (called periodically by the client)."""
        presence, created = Presence.objects.update_or_create(
            user=request.user,
            defaults={
                'organization_id': org_id,
                'status': request.data.get('status', 'online'),
                'current_resource_type': request.data.get('resource_type', ''),
                'current_resource_id': request.data.get('resource_id'),
            },
        )
        return Response(PresenceSerializer(presence).data)

    @action(detail=False, methods=['post'])
    def go_offline(self, request, org_id=None):
        """Set user as offline."""
        Presence.objects.filter(user=request.user).update(status='offline')
        return Response({'status': 'offline'})
