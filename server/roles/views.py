from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.permissions import HasResourcePermission, IsOrgAdmin
from .models import Role, ResourcePermission, RESOURCE_CHOICES
from .serializers import (
    RoleSerializer, RoleCreateSerializer,
    ResourcePermissionSerializer, BulkPermissionUpdateSerializer,
)


class RoleViewSet(viewsets.ModelViewSet):
    """
    CRUD for custom roles within an organization.
    Admin creates roles and assigns granular read/create/update/delete per resource.
    """

    permission_classes = [IsAuthenticated, IsOrgAdmin]
    rbac_resource = 'roles'

    def get_queryset(self):
        return Role.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).prefetch_related('permissions')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RoleCreateSerializer
        return RoleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def destroy(self, request, *args, **kwargs):
        role = self.get_object()
        if role.is_system:
            return Response(
                {'error': 'System roles cannot be deleted'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def set_permissions(self, request, org_id=None, pk=None):
        """
        Bulk-set permissions for a role.
        POST body:
        {
            "permissions": [
                {"resource": "campaigns", "can_read": true, "can_create": true, ...},
                ...
            ]
        }
        """
        role = self.get_object()
        if role.is_system and role.name == 'Owner':
            return Response(
                {'error': 'Owner role permissions cannot be modified'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BulkPermissionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Delete existing and recreate
        role.permissions.all().delete()
        for perm_data in serializer.validated_data['permissions']:
            perm_data.pop('id', None)
            perm_data.pop('resource_display', None)
            ResourcePermission.objects.create(role=role, **perm_data)

        return Response(RoleSerializer(role).data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, org_id=None, pk=None):
        """Duplicate a role with a new name."""
        original = self.get_object()
        new_name = request.data.get('name', f"{original.name} (Copy)")

        new_role = Role.objects.create(
            organization_id=org_id,
            name=new_name,
            description=original.description,
            created_by=request.user,
        )

        for perm in original.permissions.all():
            ResourcePermission.objects.create(
                role=new_role,
                resource=perm.resource,
                can_read=perm.can_read,
                can_create=perm.can_create,
                can_update=perm.can_update,
                can_delete=perm.can_delete,
            )

        return Response(
            RoleSerializer(new_role).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['post'])
    def set_default(self, request, org_id=None, pk=None):
        """Set this role as the default for new members."""
        role = self.get_object()
        # Clear existing defaults
        Role.objects.filter(
            organization_id=org_id, is_default=True,
        ).update(is_default=False)
        role.is_default = True
        role.save(update_fields=['is_default'])
        return Response({'status': 'default_set', 'role': role.name})

    @action(detail=False, methods=['get'])
    def available_resources(self, request, org_id=None):
        """Return the list of resources that can be permissioned."""
        return Response([
            {'key': k, 'label': v} for k, v in RESOURCE_CHOICES
        ])

    @action(detail=True, methods=['get'])
    def members(self, request, org_id=None, pk=None):
        """List all members with this role."""
        role = self.get_object()
        from teams.serializers import MembershipSerializer
        members = role.members.filter(is_active=True).select_related('user', 'team')
        return Response(MembershipSerializer(members, many=True).data)
