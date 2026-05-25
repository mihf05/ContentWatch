from rest_framework import serializers
from .models import WorkflowTemplate, WorkflowStep, WorkflowInstance, StepExecution


class WorkflowStepSerializer(serializers.ModelSerializer):
    assigned_role_name = serializers.CharField(
        source='assigned_role.name', read_only=True, default=None,
    )

    class Meta:
        model = WorkflowStep
        fields = [
            'id', 'name', 'description', 'order', 'step_type',
            'assigned_role', 'assigned_role_name', 'requires_approval',
            'auto_advance', 'estimated_duration_hours', 'config',
        ]


class WorkflowTemplateSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(many=True, read_only=True)
    step_count = serializers.SerializerMethodField()

    class Meta:
        model = WorkflowTemplate
        fields = [
            'id', 'organization', 'name', 'description', 'is_active',
            'steps', 'step_count', 'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['organization', 'created_by', 'created_at', 'updated_at']

    def get_step_count(self, obj):
        return obj.steps.count()


class WorkflowTemplateCreateSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(many=True, required=False)

    class Meta:
        model = WorkflowTemplate
        fields = ['name', 'description', 'is_active', 'steps']

    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        request = self.context['request']
        org_id = self.context['view'].kwargs['org_id']

        template = WorkflowTemplate.objects.create(
            organization_id=org_id,
            created_by=request.user,
            **validated_data,
        )

        for step_data in steps_data:
            WorkflowStep.objects.create(template=template, **step_data)

        return template

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if steps_data is not None:
            instance.steps.all().delete()
            for step_data in steps_data:
                WorkflowStep.objects.create(template=instance, **step_data)

        return instance


class StepExecutionSerializer(serializers.ModelSerializer):
    step_name = serializers.CharField(source='step.name', read_only=True)
    assigned_to_email = serializers.CharField(
        source='assigned_to.email', read_only=True, default=None,
    )

    class Meta:
        model = StepExecution
        fields = [
            'id', 'step', 'step_name', 'assigned_to', 'assigned_to_email',
            'status', 'notes', 'output', 'started_at', 'completed_at', 'created_at',
        ]
        read_only_fields = ['step', 'created_at']


class WorkflowInstanceSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    current_step_name = serializers.CharField(
        source='current_step.name', read_only=True, default=None,
    )
    executions = StepExecutionSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = WorkflowInstance
        fields = [
            'id', 'template', 'template_name', 'organization', 'title',
            'description', 'current_step', 'current_step_name', 'status',
            'resource_type', 'resource_id', 'executions', 'progress',
            'started_by', 'started_at', 'completed_at', 'metadata',
        ]
        read_only_fields = [
            'organization', 'current_step', 'started_by',
            'started_at', 'completed_at',
        ]

    def get_progress(self, obj):
        total = obj.template.steps.count()
        if total == 0:
            return 0
        completed = obj.executions.filter(status='completed').count()
        return round((completed / total) * 100)


class WorkflowInstanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowInstance
        fields = ['template', 'title', 'description', 'resource_type', 'resource_id', 'metadata']

    def create(self, validated_data):
        request = self.context['request']
        org_id = self.context['view'].kwargs['org_id']
        template = validated_data['template']

        instance = WorkflowInstance.objects.create(
            organization_id=org_id,
            started_by=request.user,
            **validated_data,
        )

        # Initialize step executions for all steps
        first_step = template.steps.order_by('order').first()
        if first_step:
            instance.current_step = first_step
            instance.save(update_fields=['current_step'])

        for step in template.steps.all():
            StepExecution.objects.create(
                instance=instance,
                step=step,
                status='pending',
            )

        return instance
