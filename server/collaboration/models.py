from django.conf import settings
from django.db import models


class Activity(models.Model):
    """
    Audit log / activity feed entry.
    Every meaningful action in the system creates an Activity record.
    """

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='activities',
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='activities',
    )
    action = models.CharField(
        max_length=50,
        help_text='Verb: created, updated, deleted, approved, rejected, commented, etc.',
    )
    resource_type = models.CharField(max_length=50, help_text='e.g. campaign, asset, workflow')
    resource_id = models.PositiveIntegerField()
    resource_title = models.CharField(max_length=255, blank=True)
    details = models.JSONField(default=dict, blank=True, help_text='Extra context')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'activities'
        indexes = [
            models.Index(fields=['organization', 'resource_type', 'resource_id']),
            models.Index(fields=['organization', '-created_at']),
        ]

    def __str__(self):
        return f"{self.actor} {self.action} {self.resource_type} #{self.resource_id}"


class Comment(models.Model):
    """
    Generic threaded comment that can be attached to any resource.
    (Separate from AssetComment which has spatial annotation.)
    """

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments',
    )
    resource_type = models.CharField(max_length=50)
    resource_id = models.PositiveIntegerField()
    content = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='replies',
    )
    is_edited = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['resource_type', 'resource_id']),
        ]

    def __str__(self):
        return f"Comment by {self.author} on {self.resource_type} #{self.resource_id}"


class Notification(models.Model):
    """
    In-app notification delivered to a specific user.
    """

    TYPE_CHOICES = [
        ('approval_requested', 'Approval Requested'),
        ('approval_decided', 'Approval Decision'),
        ('comment_added', 'New Comment'),
        ('mention', 'Mentioned'),
        ('assignment', 'Task Assigned'),
        ('status_change', 'Status Changed'),
        ('invitation', 'Invitation'),
        ('deadline', 'Deadline Reminder'),
        ('system', 'System'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications',
    )
    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='notifications',
    )
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    resource_type = models.CharField(max_length=50, blank=True)
    resource_id = models.PositiveIntegerField(null=True, blank=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='triggered_notifications',
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f"[{self.notification_type}] {self.title}"


class Presence(models.Model):
    """
    Track user online status and what resource they're currently viewing.
    Updated via WebSocket heartbeats.
    """

    STATUS_CHOICES = [
        ('online', 'Online'),
        ('away', 'Away'),
        ('busy', 'Do Not Disturb'),
        ('offline', 'Offline'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='presence',
    )
    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE,
        null=True, blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    current_resource_type = models.CharField(max_length=50, blank=True)
    current_resource_id = models.PositiveIntegerField(null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} — {self.get_status_display()}"
