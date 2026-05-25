from django.conf import settings
from django.db import models


class WorkflowTemplate(models.Model):
    """
    A reusable workflow blueprint (e.g. "Content Review Pipeline", "Campaign Launch").
    Contains ordered steps that get instantiated when applied to a campaign or asset.
    """

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='workflow_templates',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    """
    A single step in a workflow template.
    Steps are ordered and can be of different types.
    """

    STEP_TYPE_CHOICES = [
        ('task', 'Task'),
        ('review', 'Review'),
        ('approval', 'Approval'),
        ('notification', 'Notification'),
        ('checkpoint', 'Checkpoint'),
    ]

    template = models.ForeignKey(
        WorkflowTemplate, on_delete=models.CASCADE, related_name='steps',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()
    step_type = models.CharField(max_length=30, choices=STEP_TYPE_CHOICES, default='task')
    assigned_role = models.ForeignKey(
        'roles.Role', on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text='Role responsible for this step',
    )
    requires_approval = models.BooleanField(default=False)
    auto_advance = models.BooleanField(
        default=False,
        help_text='Automatically advance to next step on completion',
    )
    estimated_duration_hours = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Expected hours to complete this step',
    )
    config = models.JSONField(
        default=dict, blank=True,
        help_text='Step-specific configuration (e.g. approval rules, notification templates)',
    )

    class Meta:
        ordering = ['order']
        unique_together = ['template', 'order']

    def __str__(self):
        return f"#{self.order} {self.name}"


class WorkflowInstance(models.Model):
    """
    A running instance of a workflow template applied to a specific piece of work.
    Tracks progress through the template's steps.
    """

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    template = models.ForeignKey(
        WorkflowTemplate, on_delete=models.CASCADE, related_name='instances',
    )
    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='workflow_instances',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    current_step = models.ForeignKey(
        WorkflowStep, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='+',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Generic link to the resource this workflow is for
    resource_type = models.CharField(
        max_length=50, blank=True,
        help_text='e.g. campaign, asset, deliverable',
    )
    resource_id = models.PositiveIntegerField(null=True, blank=True)

    started_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def advance(self):
        """Move to the next step in the workflow."""
        if not self.current_step:
            return False

        next_steps = self.template.steps.filter(
            order__gt=self.current_step.order,
        ).order_by('order')

        if next_steps.exists():
            self.current_step = next_steps.first()
            self.save(update_fields=['current_step'])
            return True
        else:
            # All steps completed
            from django.utils import timezone
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save(update_fields=['status', 'completed_at'])
            return False


class StepExecution(models.Model):
    """
    Tracks the execution of a single step within a workflow instance.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
        ('blocked', 'Blocked'),
        ('failed', 'Failed'),
    ]

    instance = models.ForeignKey(
        WorkflowInstance, on_delete=models.CASCADE, related_name='executions',
    )
    step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='step_executions',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    output = models.JSONField(default=dict, blank=True, help_text='Step output data')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['step__order']

    def __str__(self):
        return f"{self.step.name} → {self.get_status_display()}"
