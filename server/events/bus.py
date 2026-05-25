"""
Event bus: publishes events to Redis for real-time consumption.
All event emission goes through emit_event() which:
1. Persists the event to the database
2. Publishes to Redis for WebSocket consumers
3. Triggers Django signals for sync handlers
"""

import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def emit_event(
    organization_id: int,
    event_type: str,
    payload: dict = None,
    actor_id: int = None,
    resource_type: str = '',
    resource_id: int = None,
):
    """
    Central event emitter.
    Creates an Event record and publishes to Redis for real-time delivery.

    Args:
        organization_id: The org scope for this event
        event_type: Dot-notation type (e.g. 'campaign.created', 'asset.approved')
        payload: Event-specific data dict
        actor_id: User who triggered the event
        resource_type: Type of resource (e.g. 'campaign', 'asset')
        resource_id: ID of the specific resource
    """
    from events.models import Event

    event = Event.objects.create(
        organization_id=organization_id,
        event_type=event_type,
        actor_id=actor_id,
        resource_type=resource_type,
        resource_id=resource_id,
        payload=payload or {},
    )

    # Publish to Redis for WebSocket consumers
    _publish_to_redis(organization_id, event)

    # Also create activity log
    _create_activity(event)

    logger.info(f"Event emitted: {event_type} org={organization_id} resource={resource_type}#{resource_id}")
    return event


def _publish_to_redis(org_id: int, event):
    """Publish event to a Redis channel for real-time delivery."""
    try:
        import redis as redis_lib
        r = redis_lib.from_url(
            getattr(settings, 'CHANNEL_LAYERS', {}).get('default', {}).get(
                'CONFIG', {},
            ).get('hosts', [('redis', 6379)])[0]
            if isinstance(
                getattr(settings, 'CHANNEL_LAYERS', {}).get('default', {}).get(
                    'CONFIG', {},
                ).get('hosts', [('redis', 6379)])[0], str,
            )
            else f"redis://{getattr(settings, 'REDIS_HOST', 'redis')}:{getattr(settings, 'REDIS_PORT', 6379)}/0",
        )
        channel = f"org.{org_id}.events"
        r.publish(channel, json.dumps({
            'event_type': event.event_type,
            'resource_type': event.resource_type,
            'resource_id': event.resource_id,
            'actor_id': event.actor_id,
            'payload': event.payload,
            'created_at': event.created_at.isoformat(),
        }))
    except Exception as e:
        logger.warning(f"Failed to publish event to Redis: {e}")


def _create_activity(event):
    """Create an Activity record from the event for the audit log."""
    try:
        from collaboration.models import Activity

        # Extract action from event_type (e.g. 'campaign.created' → 'created')
        parts = event.event_type.split('.')
        action = parts[-1] if len(parts) > 1 else event.event_type

        Activity.objects.create(
            organization_id=event.organization_id,
            actor_id=event.actor_id,
            action=action,
            resource_type=event.resource_type,
            resource_id=event.resource_id or 0,
            resource_title=event.payload.get('title', ''),
            details=event.payload,
        )
    except Exception as e:
        logger.warning(f"Failed to create activity from event: {e}")
