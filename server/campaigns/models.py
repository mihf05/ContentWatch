from django.conf import settings
from django.db import models


class Campaign(models.Model):
    """
    A campaign (brand deal, content series, product launch, etc.).
    Campaigns flow through stages and produce deliverables.
    """

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='campaigns',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    brief = models.TextField(blank=True, help_text='Campaign brief / client requirements')

    # Optional link to a client org (for agency workflows)
    client = models.ForeignKey(
        'teams.Organization', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='client_campaigns',
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    workflow = models.ForeignKey(
        'workflows.WorkflowTemplate', on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text='Workflow template attached to this campaign',
    )
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_campaigns',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class CampaignStage(models.Model):
    """
    A stage within a campaign pipeline (e.g. "Ideation", "Production", "Review", "Publish").
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='stages',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_stages',
    )
    assigned_team = models.ForeignKey(
        'teams.Team', on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ['campaign', 'order']

    def __str__(self):
        return f"{self.campaign.name} → {self.name}"


class CampaignDeliverable(models.Model):
    """
    A specific content deliverable within a campaign
    (e.g. "Instagram Reel #1", "YouTube Sponsor Segment").
    """

    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter / X'),
        ('linkedin', 'LinkedIn'),
        ('facebook', 'Facebook'),
        ('other', 'Other'),
    ]

    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('short_video', 'Short Video / Reel'),
        ('image', 'Image / Carousel'),
        ('story', 'Story'),
        ('post', 'Text Post'),
        ('article', 'Article / Blog'),
        ('live', 'Live Stream'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('revision', 'Needs Revision'),
        ('approved', 'Approved'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
    ]

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='deliverables',
    )
    stage = models.ForeignKey(
        CampaignStage, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='deliverables',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateTimeField(null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_deliverables',
    )
    specs = models.JSONField(
        default=dict, blank=True,
        help_text='Platform-specific specs (dimensions, duration, hashtags, etc.)',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"
