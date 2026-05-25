"""
Django signals for the teams app.
Auto-create system roles when an organization is created via signal
(in case org is created outside the serializer path).
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Organization

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Organization)
def on_organization_created(sender, instance, created, **kwargs):
    """Emit event when a new organization is created."""
    if not created:
        return

    try:
        from events.bus import emit_event
        emit_event(
            organization_id=instance.id,
            event_type='organization.created',
            payload={
                'name': instance.name,
                'org_type': instance.org_type,
            },
            actor_id=instance.owner_id,
            resource_type='organization',
            resource_id=instance.id,
        )
    except Exception as e:
        logger.warning(f"Failed to emit org.created event: {e}")
