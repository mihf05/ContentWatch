from django.conf import settings
from django.db import models


class AssetFolder(models.Model):
    """
    Hierarchical folder structure for organizing assets.
    """

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='asset_folders',
    )
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children',
    )
    color = models.CharField(max_length=7, default='#6366f1')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def path(self):
        """Return the full folder path (e.g. "Root / Brand / Q2 2026")."""
        parts = [self.name]
        current = self.parent
        while current:
            parts.insert(0, current.name)
            current = current.parent
        return ' / '.join(parts)


class Asset(models.Model):
    """
    A digital asset (image, video, audio, document, design file).
    Supports versioning, tagging, and approval workflows.
    """

    ASSET_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('design', 'Design File'),
        ('font', 'Font'),
        ('archive', 'Archive'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    ]

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='assets',
    )
    folder = models.ForeignKey(
        AssetFolder, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assets',
    )
    campaign = models.ForeignKey(
        'campaigns.Campaign', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assets',
    )
    deliverable = models.ForeignKey(
        'campaigns.CampaignDeliverable', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assets',
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    asset_type = models.CharField(max_length=30, choices=ASSET_TYPE_CHOICES)
    file = models.FileField(upload_to='assets/%Y/%m/')
    file_size = models.BigIntegerField(default=0, help_text='Size in bytes')
    mime_type = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(
        default=dict, blank=True,
        help_text='Auto-extracted metadata (dimensions, duration, codec, etc.)',
    )
    current_version = models.PositiveIntegerField(default=1)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='uploaded_assets',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'asset_type']),
            models.Index(fields=['organization', 'status']),
        ]

    def __str__(self):
        return self.name


class AssetVersion(models.Model):
    """
    Versioned snapshot of an asset. Each upload creates a new version.
    """

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    file = models.FileField(upload_to='asset_versions/%Y/%m/')
    file_size = models.BigIntegerField(default=0)
    changelog = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['asset', 'version_number']
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.asset.name} v{self.version_number}"


class AssetComment(models.Model):
    """
    Comment on an asset, with optional spatial coordinates for annotation.
    Supports threaded replies.
    """

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asset_comments',
    )
    content = models.TextField()

    # Spatial annotation (for images / video frames)
    position_x = models.FloatField(null=True, blank=True, help_text='0.0–1.0 relative X')
    position_y = models.FloatField(null=True, blank=True, help_text='0.0–1.0 relative Y')
    timestamp_seconds = models.FloatField(
        null=True, blank=True,
        help_text='For video: the timestamp in seconds where this comment applies',
    )

    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='replies',
    )
    is_resolved = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.asset.name}"
