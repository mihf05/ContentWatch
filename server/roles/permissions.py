"""
Custom DRF permission classes that enforce the RBAC system.

Usage in views:
    class CampaignViewSet(viewsets.ModelViewSet):
        permission_classes = [IsAuthenticated, HasResourcePermission]
        rbac_resource = 'campaigns'   # ← matches RESOURCE_CHOICES key
"""

from rest_framework.permissions import BasePermission

from teams.models import Membership


# Map HTTP methods to RBAC action names
METHOD_ACTION_MAP = {
    'GET': 'read',
    'HEAD': 'read',
    'OPTIONS': 'read',
    'POST': 'create',
    'PUT': 'update',
    'PATCH': 'update',
    'DELETE': 'delete',
}


def get_org_id_from_request(request, view):
    """
    Extract the organization ID from the request.
    Looks in: URL kwargs → query params → request body → header.
    """
    # 1. URL kwargs (e.g. /api/orgs/<org_id>/campaigns/)
    org_id = view.kwargs.get('org_id')
    if org_id:
        return org_id

    # 2. Query parameter
    org_id = request.query_params.get('org_id') or request.query_params.get('organization')
    if org_id:
        return org_id

    # 3. Request body (for POST/PUT/PATCH)
    if hasattr(request, 'data') and request.data:
        org_id = request.data.get('organization')
        if org_id:
            return org_id

    # 4. Custom header
    org_id = request.META.get('HTTP_X_ORGANIZATION_ID')
    return org_id


def get_membership(user, org_id):
    """Get the active membership for user in org, with role prefetched."""
    if not user or not user.is_authenticated or not org_id:
        return None
    try:
        return Membership.objects.select_related('role').get(
            user=user,
            organization_id=org_id,
            is_active=True,
        )
    except Membership.DoesNotExist:
        return None


class HasResourcePermission(BasePermission):
    """
    Checks the user's role-based permission for the resource declared on the view.

    The view MUST declare:
        rbac_resource = '<resource_key>'   (e.g. 'campaigns', 'assets')

    The organization is resolved from the request context.
    Org owners always get full access.
    """

    message = 'You do not have permission to perform this action on this resource.'

    def has_permission(self, request, view):
        resource = getattr(view, 'rbac_resource', None)
        if not resource:
            # No resource declared — allow (view is ungated)
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        # Superusers bypass RBAC
        if request.user.is_superuser:
            return True

        org_id = get_org_id_from_request(request, view)
        if not org_id:
            self.message = 'Organization context is required. Pass org_id in URL, query, body, or X-Organization-Id header.'
            return False

        membership = get_membership(request.user, org_id)
        if not membership:
            self.message = 'You are not a member of this organization.'
            return False

        # Org owner has full access
        if membership.organization.owner_id == request.user.id:
            return True

        if not membership.role:
            self.message = 'No role assigned. Contact your organization admin.'
            return False

        action = METHOD_ACTION_MAP.get(request.method, 'read')
        if not membership.role.has_permission(resource, action):
            self.message = f'Your role "{membership.role.name}" does not have {action} access to {resource}.'
            return False

        return True


class IsOrgMember(BasePermission):
    """Simply checks that the user is an active member of the organization."""

    message = 'You must be a member of this organization.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        org_id = get_org_id_from_request(request, view)
        if not org_id:
            return False

        return Membership.objects.filter(
            user=request.user,
            organization_id=org_id,
            is_active=True,
        ).exists()


class IsOrgOwner(BasePermission):
    """Checks that the user is the owner of the organization."""

    message = 'Only the organization owner can perform this action.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        org_id = get_org_id_from_request(request, view)
        if not org_id:
            return False

        from teams.models import Organization
        return Organization.objects.filter(
            id=org_id,
            owner=request.user,
        ).exists()


class IsOrgAdmin(BasePermission):
    """Checks that the user has admin-level role (can manage roles, members, settings)."""

    message = 'Admin privileges required.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        org_id = get_org_id_from_request(request, view)
        if not org_id:
            return False

        membership = get_membership(request.user, org_id)
        if not membership:
            return False

        # Owner is always admin
        if membership.organization.owner_id == request.user.id:
            return True

        # Check if role has full CRUD on 'roles' resource (admin indicator)
        if membership.role:
            return (
                membership.role.has_permission('roles', 'create')
                and membership.role.has_permission('roles', 'update')
                and membership.role.has_permission('roles', 'delete')
            )

        return False
