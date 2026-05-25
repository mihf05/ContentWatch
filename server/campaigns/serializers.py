from rest_framework import serializers
from .models import Campaign, CampaignStage, CampaignDeliverable


class CampaignStageSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.CharField(
        source='assigned_to.email', read_only=True, default=None,
    )
    deliverable_count = serializers.SerializerMethodField()

    class Meta:
        model = CampaignStage
        fields = [
            'id', 'campaign', 'name', 'description', 'order', 'status',
            'due_date', 'assigned_to', 'assigned_to_email', 'assigned_team',
            'deliverable_count', 'completed_at', 'config',
        ]
        read_only_fields = ['campaign', 'completed_at']

    def get_deliverable_count(self, obj):
        return obj.deliverables.count()


class CampaignDeliverableSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.CharField(
        source='assigned_to.email', read_only=True, default=None,
    )

    class Meta:
        model = CampaignDeliverable
        fields = [
            'id', 'campaign', 'stage', 'title', 'description',
            'platform', 'content_type', 'status',
            'due_date', 'publish_date',
            'assigned_to', 'assigned_to_email', 'specs',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['campaign', 'created_at', 'updated_at']


class CampaignSerializer(serializers.ModelSerializer):
    stages = CampaignStageSerializer(many=True, read_only=True)
    deliverables = CampaignDeliverableSerializer(many=True, read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True, default=None)
    client_name = serializers.CharField(source='client.name', read_only=True, default=None)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id', 'organization', 'name', 'description', 'brief',
            'client', 'client_name', 'status', 'priority',
            'budget', 'currency', 'start_date', 'end_date',
            'workflow', 'tags', 'metadata',
            'stages', 'deliverables', 'progress',
            'created_by', 'created_by_email', 'created_at', 'updated_at',
        ]
        read_only_fields = ['organization', 'created_by', 'created_at', 'updated_at']

    def get_progress(self, obj):
        total = obj.deliverables.count()
        if total == 0:
            return 0
        done = obj.deliverables.filter(status__in=['approved', 'published']).count()
        return round((done / total) * 100)


class CampaignListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views (no nested stages/deliverables)."""
    client_name = serializers.CharField(source='client.name', read_only=True, default=None)
    deliverable_count = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'status', 'priority', 'client', 'client_name',
            'start_date', 'end_date', 'deliverable_count', 'progress',
            'created_at',
        ]

    def get_deliverable_count(self, obj):
        return obj.deliverables.count()

    def get_progress(self, obj):
        total = obj.deliverables.count()
        if total == 0:
            return 0
        done = obj.deliverables.filter(status__in=['approved', 'published']).count()
        return round((done / total) * 100)


class CampaignCreateSerializer(serializers.ModelSerializer):
    stages = CampaignStageSerializer(many=True, required=False)

    class Meta:
        model = Campaign
        fields = [
            'name', 'description', 'brief', 'client', 'status', 'priority',
            'budget', 'currency', 'start_date', 'end_date',
            'workflow', 'tags', 'metadata', 'stages',
        ]

    def create(self, validated_data):
        stages_data = validated_data.pop('stages', [])
        request = self.context['request']
        org_id = self.context['view'].kwargs['org_id']

        campaign = Campaign.objects.create(
            organization_id=org_id,
            created_by=request.user,
            **validated_data,
        )

        for stage_data in stages_data:
            stage_data.pop('campaign', None)
            CampaignStage.objects.create(campaign=campaign, **stage_data)

        return campaign
