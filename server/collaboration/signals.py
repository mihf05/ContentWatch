"""
Django signals for the collaboration app.
Emits events when notifications are created, comments added, etc.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


# We register signal handlers here so they're loaded via AppConfig.ready()
# The actual heavy lifting is done in events.handlers
# This file mostly handles WebSocket pushes for real-time notifications.

@receiver(post_save, sender='collaboration.Notification')
def push_notification_to_websocket(sender, instance, created, **kwargs):
    """Push new notifications to the user's WebSocket channel."""
    if not created:
        return

    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.recipient_id}_notifications",
                {
                    'type': 'notification.new',
                    'data': {
                        'id': instance.id,
                        'notification_type': instance.notification_type,
                        'title': instance.title,
                        'message': instance.message,
                        'resource_type': instance.resource_type,
                        'resource_id': instance.resource_id,
                        'created_at': instance.created_at.isoformat() if instance.created_at else None,
                    },
                },
            )
    except Exception as e:
        logger.debug(f"WebSocket push skipped (channels not available): {e}")
