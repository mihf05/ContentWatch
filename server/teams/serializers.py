from rest_framework import serializers
from .models import Organization, Team, Membership, Invitation, AgencyPartnership


class OrganizationSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'slug', 'owner', 'description', 'org_type',
            'logo', 'website', 'is_active', 'member_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.memberships.filter(is_active=True).count()


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'slug', 'description', 'org_type', 'logo', 'website']

    def create(self, validated_data):
        user = self.context['request'].user
        org = Organization.objects.create(owner=user, **validated_data)
        # Auto-create an "Owner" system role and membership
        from roles.models import Role
        owner_role = Role.objects.create(
            organization=org,
            name='Owner',
            description='Full access — organization owner',
            is_system=True,
            created_by=user,
        )
        owner_role.set_full_access()

        # Also create default roles
        admin_role = Role.objects.create(
            organization=org,
            name='Admin',
            description='Administrative access',
            is_system=True,
            created_by=user,
        )
        admin_role.set_full_access()

        member_role = Role.objects.create(
            organization=org,
            name='Member',
            description='Standard team member',
            is_default=True,
            created_by=user,
        )
        # Members get read on everything, create/update on campaigns, assets, workflows
        from roles.models import ResourcePermission, RESOURCE_CHOICES
        for resource_key, _ in RESOURCE_CHOICES:
            ResourcePermission.objects.create(
                role=member_role,
                resource=resource_key,
                can_read=True,
                can_create=resource_key in ('campaigns', 'assets', 'workflows', 'messaging', 'collaboration'),
                can_update=resource_key in ('campaigns', 'assets', 'workflows', 'messaging', 'collaboration'),
                can_delete=False,
            )

        viewer_role = Role.objects.create(
            organization=org,
            name='Viewer',
            description='Read-only access',
            created_by=user,
        )
        for resource_key, _ in RESOURCE_CHOICES:
            ResourcePermission.objects.create(
                role=viewer_role,
                resource=resource_key,
                can_read=True,
                can_create=False,
                can_update=False,
                can_delete=False,
            )

        # Create membership for the owner
        Membership.objects.create(
            user=user,
            organization=org,
            role=owner_role,
        )

        return org


class TeamSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id', 'organization', 'name', 'description', 'color',
            'member_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['organization', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.filter(is_active=True).count()


class MembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    role_name = serializers.CharField(source='role.name', read_only=True, default=None)
    team_name = serializers.CharField(source='team.name', read_only=True, default=None)

    class Meta:
        model = Membership
        fields = [
            'id', 'user', 'user_email', 'user_name', 'organization',
            'team', 'team_name', 'role', 'role_name', 'title',
            'is_active', 'joined_at',
        ]
        read_only_fields = ['user', 'organization', 'joined_at']

    def get_user_name(self, obj):
        u = obj.user
        return f"{u.first_name} {u.last_name}".strip() or u.email


class InvitationSerializer(serializers.ModelSerializer):
    invited_by_email = serializers.CharField(source='invited_by.email', read_only=True)

    class Meta:
        model = Invitation
        fields = [
            'id', 'organization', 'email', 'role', 'team',
            'invited_by', 'invited_by_email', 'token',
            'status', 'message', 'created_at', 'expires_at', 'is_expired',
        ]
        read_only_fields = [
            'organization', 'invited_by', 'token', 'status', 'created_at',
        ]


class InvitationCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role_id = serializers.IntegerField(required=False, allow_null=True)
    team_id = serializers.IntegerField(required=False, allow_null=True)
    message = serializers.CharField(required=False, allow_blank=True, default='')


class InvitationAcceptSerializer(serializers.Serializer):
    token = serializers.UUIDField()


class AgencyPartnershipSerializer(serializers.ModelSerializer):
    agency_name = serializers.CharField(source='agency.name', read_only=True)
    partner_name = serializers.CharField(source='partner.name', read_only=True)

    class Meta:
        model = AgencyPartnership
        fields = [
            'id', 'agency', 'agency_name', 'partner', 'partner_name',
            'status', 'contract_details', 'revenue_share_percent',
            'started_at', 'ends_at', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
