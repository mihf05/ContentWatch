from rest_framework import serializers
from .models import Role, ResourcePermission, RESOURCE_CHOICES


class ResourcePermissionSerializer(serializers.ModelSerializer):
    resource_display = serializers.CharField(source='get_resource_display', read_only=True)

    class Meta:
        model = ResourcePermission
        fields = [
            'id', 'resource', 'resource_display',
            'can_read', 'can_create', 'can_update', 'can_delete',
        ]


class RoleSerializer(serializers.ModelSerializer):
    permissions = ResourcePermissionSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id', 'organization', 'name', 'description',
            'is_system', 'is_default', 'permissions', 'member_count',
            'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['organization', 'is_system', 'created_by', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.filter(is_active=True).count()


class RoleCreateSerializer(serializers.ModelSerializer):
    """
    Create a role with inline permissions.
    Accepts:
    {
        "name": "Editor",
        "description": "...",
        "permissions": [
            {"resource": "campaigns", "can_read": true, "can_create": true, "can_update": true, "can_delete": false},
            {"resource": "assets", "can_read": true, "can_create": true, "can_update": true, "can_delete": false},
            ...
        ]
    }
    """

    permissions = ResourcePermissionSerializer(many=True, required=False)

    class Meta:
        model = Role
        fields = ['name', 'description', 'is_default', 'permissions']

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        request = self.context['request']
        org_id = self.context['view'].kwargs['org_id']

        role = Role.objects.create(
            organization_id=org_id,
            created_by=request.user,
            **validated_data,
        )

        for perm_data in permissions_data:
            # Remove read-only fields if present
            perm_data.pop('id', None)
            perm_data.pop('resource_display', None)
            ResourcePermission.objects.create(role=role, **perm_data)

        return role

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('permissions', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if permissions_data is not None:
            # Replace all permissions
            instance.permissions.all().delete()
            for perm_data in permissions_data:
                perm_data.pop('id', None)
                perm_data.pop('resource_display', None)
                ResourcePermission.objects.create(role=instance, **perm_data)

        return instance


class BulkPermissionUpdateSerializer(serializers.Serializer):
    """
    Update permissions for a role in bulk.
    [
        {"resource": "campaigns", "can_read": true, "can_create": true, ...},
        ...
    ]
    """

    permissions = ResourcePermissionSerializer(many=True)


class AvailableResourcesSerializer(serializers.Serializer):
    """Returns the list of resources that can be permissioned."""

    resources = serializers.SerializerMethodField()

    def get_resources(self, obj):
        return [{'key': k, 'label': v} for k, v in RESOURCE_CHOICES]
