from rest_framework import serializers
from .models import ApprovalChain, ApprovalLevel, ApprovalRequest, ApprovalDecision


class ApprovalLevelSerializer(serializers.ModelSerializer):
    approver_role_name = serializers.CharField(
        source='approver_role.name', read_only=True, default=None,
    )
    approver_user_email = serializers.CharField(
        source='approver_user.email', read_only=True, default=None,
    )

    class Meta:
        model = ApprovalLevel
        fields = [
            'id', 'order', 'name', 'approver_role', 'approver_role_name',
            'approver_user', 'approver_user_email', 'require_all',
            'auto_approve_hours',
        ]


class ApprovalChainSerializer(serializers.ModelSerializer):
    levels = ApprovalLevelSerializer(many=True, read_only=True)
    level_count = serializers.SerializerMethodField()

    class Meta:
        model = ApprovalChain
        fields = [
            'id', 'organization', 'name', 'description', 'resource_type',
            'is_active', 'levels', 'level_count',
            'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['organization', 'created_by', 'created_at', 'updated_at']

    def get_level_count(self, obj):
        return obj.levels.count()


class ApprovalChainCreateSerializer(serializers.ModelSerializer):
    levels = ApprovalLevelSerializer(many=True, required=False)

    class Meta:
        model = ApprovalChain
        fields = ['name', 'description', 'resource_type', 'is_active', 'levels']

    def create(self, validated_data):
        levels_data = validated_data.pop('levels', [])
        request = self.context['request']
        org_id = self.context['view'].kwargs['org_id']

        chain = ApprovalChain.objects.create(
            organization_id=org_id,
            created_by=request.user,
            **validated_data,
        )

        for level_data in levels_data:
            ApprovalLevel.objects.create(chain=chain, **level_data)

        return chain

    def update(self, instance, validated_data):
        levels_data = validated_data.pop('levels', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if levels_data is not None:
            instance.levels.all().delete()
            for level_data in levels_data:
                ApprovalLevel.objects.create(chain=instance, **level_data)

        return instance


class ApprovalDecisionSerializer(serializers.ModelSerializer):
    approver_email = serializers.CharField(source='approver.email', read_only=True)

    class Meta:
        model = ApprovalDecision
        fields = [
            'id', 'level', 'approver', 'approver_email',
            'decision', 'comment', 'decided_at',
        ]
        read_only_fields = ['approver', 'decided_at']


class ApprovalRequestSerializer(serializers.ModelSerializer):
    chain_name = serializers.CharField(source='chain.name', read_only=True)
    current_level_name = serializers.CharField(
        source='current_level.name', read_only=True, default=None,
    )
    decisions = ApprovalDecisionSerializer(many=True, read_only=True)
    requested_by_email = serializers.CharField(source='requested_by.email', read_only=True)

    class Meta:
        model = ApprovalRequest
        fields = [
            'id', 'chain', 'chain_name', 'organization',
            'resource_type', 'resource_id', 'resource_title',
            'current_level', 'current_level_name', 'status', 'priority',
            'decisions', 'notes',
            'requested_by', 'requested_by_email',
            'created_at', 'resolved_at',
        ]
        read_only_fields = [
            'organization', 'current_level', 'status',
            'requested_by', 'created_at', 'resolved_at',
        ]


class ApprovalRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = ['chain', 'resource_type', 'resource_id', 'resource_title', 'priority', 'notes']

    def create(self, validated_data):
        request = self.context['request']
        org_id = self.context['view'].kwargs['org_id']

        approval_request = ApprovalRequest.objects.create(
            organization_id=org_id,
            requested_by=request.user,
            **validated_data,
        )

        # Auto-advance to the first level
        approval_request.advance_level()
        return approval_request


class ApprovalDecisionCreateSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=ApprovalDecision.DECISION_CHOICES)
    comment = serializers.CharField(required=False, allow_blank=True, default='')
