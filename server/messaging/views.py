from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.permissions import HasResourcePermission
from .models import MessageThread, ThreadParticipant, Message, MessageReaction
from .serializers import (
    MessageThreadSerializer, MessageThreadListSerializer, MessageThreadCreateSerializer,
    ThreadParticipantSerializer,
    MessageSerializer, MessageCreateSerializer,
    MessageReactionSerializer,
)


class MessageThreadViewSet(viewsets.ModelViewSet):
    """Manage message threads."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    rbac_resource = 'messaging'

    def get_queryset(self):
        qs = MessageThread.objects.filter(
            organization_id=self.kwargs['org_id'],
            participants__user=self.request.user,
        ).distinct().prefetch_related('participants')

        # Filters
        thread_type = self.request.query_params.get('type')
        if thread_type:
            qs = qs.filter(thread_type=thread_type)

        archived = self.request.query_params.get('archived')
        if archived is not None:
            qs = qs.filter(is_archived=archived.lower() == 'true')
        else:
            qs = qs.filter(is_archived=False)

        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return MessageThreadListSerializer
        return MessageThreadSerializer

    def create(self, request, org_id=None):
        serializer = MessageThreadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        thread = MessageThread.objects.create(
            organization_id=org_id,
            title=data.get('title', ''),
            thread_type=data.get('thread_type', 'group'),
            campaign_id=data.get('campaign_id'),
            created_by=request.user,
        )

        # Add creator as admin participant
        ThreadParticipant.objects.create(
            thread=thread, user=request.user, role='admin',
        )

        # Add other participants
        for user_id in data.get('participant_ids', []):
            if user_id != request.user.id:
                ThreadParticipant.objects.get_or_create(
                    thread=thread, user_id=user_id,
                    defaults={'role': 'member'},
                )

        return Response(
            MessageThreadSerializer(thread, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['post'])
    def add_participant(self, request, org_id=None, pk=None):
        """Add a user to the thread."""
        thread = self.get_object()
        user_id = request.data.get('user_id')
        role = request.data.get('role', 'member')
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        participant, created = ThreadParticipant.objects.get_or_create(
            thread=thread, user_id=user_id,
            defaults={'role': role},
        )
        return Response(ThreadParticipantSerializer(participant).data)

    @action(detail=True, methods=['post'])
    def remove_participant(self, request, org_id=None, pk=None):
        """Remove a user from the thread."""
        thread = self.get_object()
        user_id = request.data.get('user_id')
        ThreadParticipant.objects.filter(thread=thread, user_id=user_id).delete()
        return Response({'status': 'removed'})

    @action(detail=True, methods=['post'])
    def archive(self, request, org_id=None, pk=None):
        thread = self.get_object()
        thread.is_archived = True
        thread.save(update_fields=['is_archived'])
        return Response({'status': 'archived'})

    @action(detail=True, methods=['post'])
    def unarchive(self, request, org_id=None, pk=None):
        thread = self.get_object()
        thread.is_archived = False
        thread.save(update_fields=['is_archived'])
        return Response({'status': 'unarchived'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, org_id=None, pk=None):
        """Mark all messages in thread as read for the current user."""
        thread = self.get_object()
        ThreadParticipant.objects.filter(
            thread=thread, user=request.user,
        ).update(last_read_at=timezone.now())
        return Response({'status': 'read'})


class MessageViewSet(viewsets.ModelViewSet):
    """Messages within a thread."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = MessageSerializer
    rbac_resource = 'messaging'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return Message.objects.filter(
            thread_id=self.kwargs['thread_id'],
            thread__organization_id=self.kwargs['org_id'],
            is_deleted=False,
        ).select_related('sender').prefetch_related('reactions')

    def create(self, request, org_id=None, thread_id=None):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        message = Message.objects.create(
            thread_id=thread_id,
            sender=request.user,
            content=data['content'],
            message_type=data.get('message_type', 'text'),
            file=data.get('file'),
            parent_id=data.get('parent_id'),
        )

        # Update thread timestamp
        MessageThread.objects.filter(id=thread_id).update(updated_at=timezone.now())

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED,
        )

    def perform_update(self, serializer):
        serializer.save(is_edited=True, edited_at=timezone.now())

    def destroy(self, request, *args, **kwargs):
        """Soft-delete a message."""
        message = self.get_object()
        if message.sender != request.user:
            return Response(
                {'error': 'You can only delete your own messages'},
                status=status.HTTP_403_FORBIDDEN,
            )
        message.is_deleted = True
        message.content = '[deleted]'
        message.save(update_fields=['is_deleted', 'content'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def react(self, request, org_id=None, thread_id=None, pk=None):
        """Add or toggle a reaction on a message."""
        message = self.get_object()
        emoji = request.data.get('emoji', '👍')

        reaction, created = MessageReaction.objects.get_or_create(
            message=message, user=request.user, emoji=emoji,
        )
        if not created:
            reaction.delete()
            return Response({'status': 'removed'})

        return Response(
            MessageReactionSerializer(reaction).data,
            status=status.HTTP_201_CREATED,
        )
