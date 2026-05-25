from django.conf import settings
from django.db import models


class Event(models.Model):
    """
    Immutable event record for the event-driven architecture.
    Every state change emits an event that can be consumed by handlers,
    pushed to WebSockets, or processed by Celery workers.
    """

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='events',
    )
    event_type = models.CharField(
        max_length=100, db_index=True,
        help_text='Dot-notation type: campaign.created, asset.approved, approval.decided, etc.',
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    resource_type = models.CharField(max_length=50, blank=True)
    resource_id = models.PositiveIntegerField(null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True, help_text='Event-specific data')
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'processed']),
            models.Index(fields=['organization', '-created_at']),
            models.Index(fields=['resource_type', 'resource_id']),
        ]

    def __str__(self):
        return f"[{self.event_type}] {self.resource_type}#{self.resource_id}"
