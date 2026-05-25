"""
Event signal handlers.
Connected via events.apps.EventsConfig.ready().
These handlers react to events by creating notifications, etc.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import Event

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Event)
def handle_event(sender, instance, created, **kwargs):
    """Route events to appropriate handlers based on event_type."""
    if not created:
        return

    event = instance
    event_type = event.event_type

    try:
        if event_type.startswith('approval.'):
            _handle_approval_event(event)
        elif event_type.startswith('campaign.'):
            _handle_campaign_event(event)
        elif event_type.startswith('asset.'):
            _handle_asset_event(event)
        elif event_type.startswith('message.'):
            _handle_message_event(event)
        elif event_type.startswith('invitation.'):
            _handle_invitation_event(event)

        # Mark as processed
        Event.objects.filter(id=event.id).update(processed=True)

    except Exception as e:
        logger.error(f"Error handling event {event_type}: {e}")


def _handle_approval_event(event):
    """Create notifications for approval-related events."""
    from collaboration.models import Notification

    if event.event_type == 'approval.requested':
        # Notify approvers
        payload = event.payload
        Notification.objects.create(
            recipient_id=payload.get('approver_id') or event.actor_id,
            organization_id=event.organization_id,
            notification_type='approval_requested',
            title=f"Approval requested: {payload.get('title', '')}",
            message=payload.get('notes', ''),
            resource_type=event.resource_type,
            resource_id=event.resource_id,
            actor_id=event.actor_id,
        )
    elif event.event_type == 'approval.decided':
        payload = event.payload
        Notification.objects.create(
            recipient_id=payload.get('requester_id', event.actor_id),
            organization_id=event.organization_id,
            notification_type='approval_decided',
            title=f"Approval {payload.get('decision', 'decided')}: {payload.get('title', '')}",
            message=payload.get('comment', ''),
            resource_type=event.resource_type,
            resource_id=event.resource_id,
            actor_id=event.actor_id,
        )


def _handle_campaign_event(event):
    """Notify assigned members about campaign changes."""
    from collaboration.models import Notification

    if event.event_type == 'campaign.status_changed':
        payload = event.payload
        # Notify campaign creator
        if payload.get('creator_id') and payload['creator_id'] != event.actor_id:
            Notification.objects.create(
                recipient_id=payload['creator_id'],
                organization_id=event.organization_id,
                notification_type='status_change',
                title=f"Campaign status changed to {payload.get('new_status', '')}",
                resource_type='campaign',
                resource_id=event.resource_id,
                actor_id=event.actor_id,
            )


def _handle_asset_event(event):
    """Notify on asset approvals and comments."""
    from collaboration.models import Notification

    if event.event_type == 'asset.comment_added':
        payload = event.payload
        uploader_id = payload.get('uploader_id')
        if uploader_id and uploader_id != event.actor_id:
            Notification.objects.create(
                recipient_id=uploader_id,
                organization_id=event.organization_id,
                notification_type='comment_added',
                title=f"New comment on {payload.get('asset_name', 'your asset')}",
                resource_type='asset',
                resource_id=event.resource_id,
                actor_id=event.actor_id,
            )


def _handle_message_event(event):
    """Notify thread participants about new messages."""
    from collaboration.models import Notification
    from messaging.models import ThreadParticipant

    if event.event_type == 'message.sent':
        payload = event.payload
        thread_id = payload.get('thread_id')
        if thread_id:
            participants = ThreadParticipant.objects.filter(
                thread_id=thread_id,
                is_muted=False,
            ).exclude(user_id=event.actor_id).values_list('user_id', flat=True)

            notifications = [
                Notification(
                    recipient_id=user_id,
                    organization_id=event.organization_id,
                    notification_type='comment_added',
                    title=f"New message in {payload.get('thread_title', 'a thread')}",
                    message=payload.get('preview', ''),
                    resource_type='thread',
                    resource_id=thread_id,
                    actor_id=event.actor_id,
                )
                for user_id in participants
            ]
            Notification.objects.bulk_create(notifications)


def _handle_invitation_event(event):
    """Notify about invitations."""
    from collaboration.models import Notification

    if event.event_type == 'invitation.sent':
        payload = event.payload
        # We can't notify the invitee if they're not a user yet.
        # This handler would typically trigger an email.
        logger.info(f"Invitation sent to {payload.get('email')}")
