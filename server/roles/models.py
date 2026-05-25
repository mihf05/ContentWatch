from django.conf import settings
from django.db import models


# ── Resource registry ───────────────────────────────────────────────
# Every module that should be gated by RBAC registers its resource key here.
# Admin creates a Role → attaches ResourcePermission rows for each resource.

RESOURCE_CHOICES = [
    ('campaigns', 'Campaigns'),
    ('assets', 'Assets'),
    ('workflows', 'Workflows'),
    ('approvals', 'Approvals'),
    ('teams', 'Teams'),
    ('roles', 'Roles'),
    ('messaging', 'Messaging'),
    ('collaboration', 'Collaboration'),
    ('analytics', 'Analytics'),
    ('integrations', 'Integrations'),
    ('settings', 'Settings'),
]


class Role(models.Model):
    """
    A named role scoped to an organization.
    Admin creates roles (e.g. "Editor", "Reviewer", "Client Viewer")
    and attaches granular resource-level CRUD permissions via ResourcePermission.
    """

    organization = models.ForeignKey(
        'teams.Organization',
        on_delete=models.CASCADE,
        related_name='roles',
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(
        default=False,
        help_text='System roles (Owner, Admin) cannot be deleted.',
    )
    is_default = models.BooleanField(
        default=False,
        help_text='Automatically assigned to new members if no role specified.',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['organization', 'name']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

    # ── Convenience helpers ──────────────────────────────────────────

    def has_permission(self, resource: str, action: str) -> bool:
        """
        Check if this role grants `action` on `resource`.
        action must be one of: read, create, update, delete.
        """
        try:
            perm = self.permissions.get(resource=resource)
        except ResourcePermission.DoesNotExist:
            return False
        return getattr(perm, f'can_{action}', False)

    def set_full_access(self):
        """Grant full CRUD on every resource (used for Owner / Admin roles)."""
        for resource_key, _ in RESOURCE_CHOICES:
            ResourcePermission.objects.update_or_create(
                role=self,
                resource=resource_key,
                defaults={
                    'can_read': True,
                    'can_create': True,
                    'can_update': True,
                    'can_delete': True,
                },
            )


class ResourcePermission(models.Model):
    """
    Granular permission: what a role can do on a specific resource type.
    Each row represents one resource for one role with CRUD flags.

    Example:
        Role "Editor" →
            campaigns:  read=True, create=True, update=True,  delete=False
            assets:     read=True, create=True, update=True,  delete=False
            roles:      read=True, create=False, update=False, delete=False
    """

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    resource = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    can_read = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ['role', 'resource']
        ordering = ['resource']

    def __str__(self):
        flags = []
        if self.can_read:
            flags.append('R')
        if self.can_create:
            flags.append('C')
        if self.can_update:
            flags.append('U')
        if self.can_delete:
            flags.append('D')
        return f"{self.role.name} | {self.resource}: {''.join(flags) or '—'}"
