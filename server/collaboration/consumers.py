"""
WebSocket consumers for real-time collaboration.
Handles:
- Organization-wide event feed
- Presence tracking
- Notification delivery
"""

import json
import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

logger = logging.getLogger(__name__)


class OrganizationConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for organization-wide real-time events.
    Clients connect to: ws://host/ws/org/<org_id>/

    Broadcasts:
    - Activity feed updates
    - Status changes on campaigns, assets, workflows
    - Presence updates
    """

    async def connect(self):
        self.org_id = self.scope['url_route']['kwargs']['org_id']
        self.org_group = f"org_{self.org_id}"
        user = self.scope.get('user')

        if not user or user.is_anonymous:
            await self.close()
            return

        # Verify membership
        is_member = await self._check_membership(user.id, self.org_id)
        if not is_member:
            await self.close()
            return

        await self.channel_layer.group_add(self.org_group, self.channel_name)
        await self.accept()

        # Broadcast presence
        await self._update_presence(user.id, 'online')
        await self.channel_layer.group_send(self.org_group, {
            'type': 'presence.update',
            'data': {
                'user_id': user.id,
                'status': 'online',
            },
        })

    async def disconnect(self, close_code):
        user = self.scope.get('user')
        if user and not user.is_anonymous:
            await self._update_presence(user.id, 'offline')
            await self.channel_layer.group_send(self.org_group, {
                'type': 'presence.update',
                'data': {
                    'user_id': user.id,
                    'status': 'offline',
                },
            })

        await self.channel_layer.group_discard(self.org_group, self.channel_name)

    async def receive_json(self, content):
        """Handle incoming WebSocket messages."""
        msg_type = content.get('type')

        if msg_type == 'heartbeat':
            user = self.scope.get('user')
            if user:
                await self._update_presence(
                    user.id, 'online',
                    resource_type=content.get('resource_type', ''),
                    resource_id=content.get('resource_id'),
                )

        elif msg_type == 'presence.status':
            user = self.scope.get('user')
            if user:
                new_status = content.get('status', 'online')
                await self._update_presence(user.id, new_status)
                await self.channel_layer.group_send(self.org_group, {
                    'type': 'presence.update',
                    'data': {
                        'user_id': user.id,
                        'status': new_status,
                    },
                })

    # ── Group message handlers ──────────────────────────────────────

    async def event_broadcast(self, event):
        """Broadcast an event to connected clients."""
        await self.send_json(event['data'])

    async def presence_update(self, event):
        """Broadcast presence changes."""
        await self.send_json({
            'type': 'presence.update',
            **event['data'],
        })

    async def activity_new(self, event):
        """Broadcast new activity."""
        await self.send_json({
            'type': 'activity.new',
            **event['data'],
        })

    # ── Database helpers ────────────────────────────────────────────

    @database_sync_to_async
    def _check_membership(self, user_id, org_id):
        from teams.models import Membership
        return Membership.objects.filter(
            user_id=user_id, organization_id=org_id, is_active=True,
        ).exists()

    @database_sync_to_async
    def _update_presence(self, user_id, status, resource_type='', resource_id=None):
        from collaboration.models import Presence
        Presence.objects.update_or_create(
            user_id=user_id,
            defaults={
                'organization_id': self.org_id,
                'status': status,
                'current_resource_type': resource_type,
                'current_resource_id': resource_id,
            },
        )


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """
    Per-user WebSocket for real-time notification delivery.
    Clients connect to: ws://host/ws/notifications/
    """

    async def connect(self):
        user = self.scope.get('user')
        if not user or user.is_anonymous:
            await self.close()
            return

        self.user_group = f"user_{user.id}_notifications"
        await self.channel_layer.group_add(self.user_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope.get('user')
        if user and not user.is_anonymous:
            await self.channel_layer.group_discard(
                f"user_{user.id}_notifications", self.channel_name,
            )

    async def notification_new(self, event):
        """Push a new notification to the client."""
        await self.send_json({
            'type': 'notification',
            **event['data'],
        })


class MessagingConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for real-time messaging within a thread.
    Clients connect to: ws://host/ws/org/<org_id>/threads/<thread_id>/
    """

    async def connect(self):
        self.org_id = self.scope['url_route']['kwargs']['org_id']
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group = f"thread_{self.thread_id}"
        user = self.scope.get('user')

        if not user or user.is_anonymous:
            await self.close()
            return

        # Verify participant
        is_participant = await self._check_participant(user.id, self.thread_id)
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(self.thread_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.thread_group, self.channel_name)

    async def receive_json(self, content):
        """Handle incoming messages from WebSocket clients."""
        msg_type = content.get('type')
        user = self.scope.get('user')

        if msg_type == 'message.send':
            message_data = await self._save_message(
                user_id=user.id,
                thread_id=self.thread_id,
                content_text=content.get('content', ''),
                parent_id=content.get('parent_id'),
            )
            if message_data:
                await self.channel_layer.group_send(self.thread_group, {
                    'type': 'message.new',
                    'data': message_data,
                })

        elif msg_type == 'typing.start':
            await self.channel_layer.group_send(self.thread_group, {
                'type': 'typing.indicator',
                'data': {'user_id': user.id, 'typing': True},
            })

        elif msg_type == 'typing.stop':
            await self.channel_layer.group_send(self.thread_group, {
                'type': 'typing.indicator',
                'data': {'user_id': user.id, 'typing': False},
            })

    # ── Group message handlers ──────────────────────────────────────

    async def message_new(self, event):
        await self.send_json({'type': 'message.new', **event['data']})

    async def typing_indicator(self, event):
        await self.send_json({'type': 'typing', **event['data']})

    async def message_edited(self, event):
        await self.send_json({'type': 'message.edited', **event['data']})

    async def message_deleted(self, event):
        await self.send_json({'type': 'message.deleted', **event['data']})

    async def reaction_toggled(self, event):
        await self.send_json({'type': 'reaction.toggled', **event['data']})

    # ── Database helpers ────────────────────────────────────────────

    @database_sync_to_async
    def _check_participant(self, user_id, thread_id):
        from messaging.models import ThreadParticipant
        return ThreadParticipant.objects.filter(
            user_id=user_id, thread_id=thread_id,
        ).exists()

    @database_sync_to_async
    def _save_message(self, user_id, thread_id, content_text, parent_id=None):
        from messaging.models import Message, MessageThread
        from django.utils import timezone

        try:
            message = Message.objects.create(
                thread_id=thread_id,
                sender_id=user_id,
                content=content_text,
                parent_id=parent_id,
            )
            MessageThread.objects.filter(id=thread_id).update(updated_at=timezone.now())

            return {
                'id': message.id,
                'sender_id': user_id,
                'content': message.content,
                'message_type': message.message_type,
                'parent_id': message.parent_id,
                'created_at': message.created_at.isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to save WebSocket message: {e}")
            return None
