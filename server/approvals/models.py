from django.conf import settings
from django.db import models


class ApprovalChain(models.Model):
    """
    A reusable approval pipeline with multiple levels.
    Attached to a resource type so the right chain fires automatically.
    """

    RESOURCE_TYPE_CHOICES = [
        ('campaign', 'Campaign'),
        ('asset', 'Asset'),
        ('deliverable', 'Deliverable'),
        ('content', 'Content'),
        ('workflow', 'Workflow'),
    ]

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='approval_chains',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"


class ApprovalLevel(models.Model):
    """
    One level in an approval chain.
    Levels are processed in order; each level can require a specific role or user.
    """

    chain = models.ForeignKey(
        ApprovalChain, on_delete=models.CASCADE, related_name='levels',
    )
    order = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    approver_role = models.ForeignKey(
        'roles.Role', on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text='Any member with this role can approve',
    )
    approver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text='Specific user who must approve (overrides role)',
    )
    require_all = models.BooleanField(
        default=False,
        help_text='If True, ALL eligible approvers must approve. Otherwise, any one suffices.',
    )
    auto_approve_hours = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Auto-approve if no decision within this many hours',
    )

    class Meta:
        ordering = ['order']
        unique_together = ['chain', 'order']

    def __str__(self):
        return f"Level {self.order}: {self.name}"


class ApprovalRequest(models.Model):
    """
    A concrete approval request for a specific resource.
    Moves through the chain's levels until approved, rejected, or cancelled.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    chain = models.ForeignKey(
        ApprovalChain, on_delete=models.CASCADE, related_name='requests',
    )
    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='approval_requests',
    )

    # Generic reference to the resource being approved
    resource_type = models.CharField(max_length=50)
    resource_id = models.PositiveIntegerField()
    resource_title = models.CharField(max_length=255, blank=True)

    current_level = models.ForeignKey(
        ApprovalLevel, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='+',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_approvals',
    )
    notes = models.TextField(blank=True, help_text='Submission notes')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Approval #{self.pk}: {self.resource_title or self.resource_type}"

    def advance_level(self):
        """Move to the next approval level, or mark as approved if all levels passed."""
        if not self.current_level:
            first_level = self.chain.levels.order_by('order').first()
            if first_level:
                self.current_level = first_level
                self.status = 'in_review'
                self.save(update_fields=['current_level', 'status'])
            return

        next_levels = self.chain.levels.filter(
            order__gt=self.current_level.order,
        ).order_by('order')

        if next_levels.exists():
            self.current_level = next_levels.first()
            self.save(update_fields=['current_level'])
        else:
            from django.utils import timezone
            self.status = 'approved'
            self.resolved_at = timezone.now()
            self.save(update_fields=['status', 'resolved_at'])


class ApprovalDecision(models.Model):
    """
    Individual decision by an approver at a specific level.
    """

    DECISION_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revision_requested', 'Revision Requested'),
        ('abstained', 'Abstained'),
    ]

    request = models.ForeignKey(
        ApprovalRequest, on_delete=models.CASCADE, related_name='decisions',
    )
    level = models.ForeignKey(ApprovalLevel, on_delete=models.CASCADE)
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approval_decisions',
    )
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    comment = models.TextField(blank=True)
    decided_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['decided_at']
        unique_together = ['request', 'level', 'approver']

    def __str__(self):
        return f"{self.approver} → {self.get_decision_display()}"
