from django.conf import settings
from django.db import models


class MessageThread(models.Model):
    """
    A conversation thread — can be DM, group chat, campaign-specific, or client channel.
    """

    THREAD_TYPE_CHOICES = [
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
        ('campaign', 'Campaign Thread'),
        ('client', 'Client Communication'),
    ]

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='threads',
    )
    title = models.CharField(max_length=255, blank=True)
    thread_type = models.CharField(max_length=20, choices=THREAD_TYPE_CHOICES, default='group')
    campaign = models.ForeignKey(
        'campaigns.Campaign', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='threads',
    )
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_threads',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title or f"Thread #{self.pk}"

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()


class ThreadParticipant(models.Model):
    """
    A participant in a message thread with their role and read state.
    """

    ROLE_CHOICES = [
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('observer', 'Observer'),
    ]

    thread = models.ForeignKey(
        MessageThread, on_delete=models.CASCADE, related_name='participants',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='thread_participations',
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    last_read_at = models.DateTimeField(null=True, blank=True)
    is_muted = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['thread', 'user']
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.user} in {self.thread}"

    @property
    def unread_count(self):
        qs = self.thread.messages.all()
        if self.last_read_at:
            qs = qs.filter(created_at__gt=self.last_read_at)
        return qs.exclude(sender=self.user).count()


class Message(models.Model):
    """
    A single message in a thread.
    """

    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('file', 'File Attachment'),
        ('image', 'Image'),
        ('system', 'System Message'),
        ('link', 'Link Preview'),
    ]

    thread = models.ForeignKey(
        MessageThread, on_delete=models.CASCADE, related_name='messages',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages',
    )
    content = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    file = models.FileField(upload_to='messages/%Y/%m/', null=True, blank=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)

    # Reply threading
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='replies',
    )

    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['thread', 'created_at']),
        ]

    def __str__(self):
        preview = self.content[:50] if self.content else '[file]'
        return f"{self.sender}: {preview}"


class MessageReaction(models.Model):
    """
    Emoji reaction on a message.
    """

    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='reactions',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['message', 'user', 'emoji']

    def __str__(self):
        return f"{self.user} reacted {self.emoji}"
