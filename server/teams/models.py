import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Organization(models.Model):
    """
    Top-level entity representing a creator team, agency, or brand.
    All resources are scoped to an organization for multi-tenancy.
    """

    ORG_TYPE_CHOICES = [
        ('creator', 'Creator Team'),
        ('agency', 'Agency'),
        ('brand', 'Brand / Client'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_organizations',
    )
    description = models.TextField(blank=True)
    org_type = models.CharField(max_length=20, choices=ORG_TYPE_CHOICES, default='creator')
    logo = models.ImageField(upload_to='org_logos/', null=True, blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_org_type_display()})"


class Team(models.Model):
    """
    A sub-group within an organization (e.g. "Video Editors", "Social Media").
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='teams',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6366f1', help_text='Hex color for UI')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['organization', 'name']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} @ {self.organization.name}"


class Membership(models.Model):
    """
    Links a user to an organization with a role.
    A user may belong to multiple organizations but has exactly one membership per org.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='memberships',
    )
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='members',
    )
    role = models.ForeignKey(
        'roles.Role', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='members',
    )
    title = models.CharField(max_length=255, blank=True, help_text='Job title')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'organization']
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user} → {self.organization.name}"


class Invitation(models.Model):
    """
    Pending invitation to join an organization.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='invitations',
    )
    email = models.EmailField()
    role = models.ForeignKey(
        'roles.Role', on_delete=models.SET_NULL, null=True, blank=True,
    )
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True,
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations',
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text='Personal message in the invite')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invite {self.email} → {self.organization.name}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)


class AgencyPartnership(models.Model):
    """
    Represents a partnership between an agency and a creator team or brand.
    Enables the creator-agency ecosystem.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('terminated', 'Terminated'),
    ]

    agency = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name='agency_partnerships',
        limit_choices_to={'org_type': 'agency'},
    )
    partner = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name='partner_of_agencies',
        help_text='Creator team or brand partnered with this agency',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    contract_details = models.JSONField(default=dict, blank=True)
    revenue_share_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    started_at = models.DateField(null=True, blank=True)
    ends_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['agency', 'partner']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agency.name} ↔ {self.partner.name}"
