from rest_framework import serializers
from .models import (
    AIAgentProfile,
    AIKnowledgeDocument,
    AIPipelineTemplate,
    AIPipelineStep,
    AIPipelineRun,
    AIStepRun,
)


class AIAgentProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = AIAgentProfile
        fields = [
            'id', 'organization', 'name', 'role', 'role_display',
            'system_prompt', 'temperature', 'is_default', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'organization', 'created_at', 'updated_at']


class AIKnowledgeDocumentSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = AIKnowledgeDocument
        fields = [
            'id', 'organization', 'title', 'content', 'category',
            'category_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'organization', 'created_at', 'updated_at']


class AIPipelineStepSerializer(serializers.ModelSerializer):
    step_type_display = serializers.CharField(source='get_step_type_display', read_only=True)
    agent_name = serializers.CharField(source='agent.name', read_only=True)

    class Meta:
        model = AIPipelineStep
        fields = [
            'id', 'template', 'agent', 'agent_name', 'name',
            'step_type', 'step_type_display', 'order', 'prompt_template'
        ]
        read_only_fields = ['id']


class AIPipelineTemplateSerializer(serializers.ModelSerializer):
    steps = AIPipelineStepSerializer(many=True, read_only=True)

    class Meta:
        model = AIPipelineTemplate
        fields = ['id', 'organization', 'name', 'description', 'is_active', 'steps', 'created_at', 'updated_at']
        read_only_fields = ['id', 'organization', 'created_at', 'updated_at']


class AIStepRunSerializer(serializers.ModelSerializer):
    step_name = serializers.CharField(source='step.name', read_only=True)
    step_type = serializers.CharField(source='step.step_type', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AIStepRun
        fields = [
            'id', 'pipeline_run', 'step', 'step_name', 'step_type',
            'status', 'status_display', 'agent_thoughts', 'output_content',
            'started_at', 'completed_at'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at']


class AIPipelineRunSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    triggered_by_username = serializers.CharField(source='triggered_by.username', read_only=True)
    step_runs = AIStepRunSerializer(many=True, read_only=True)

    class Meta:
        model = AIPipelineRun
        fields = [
            'id', 'organization', 'template', 'template_name', 'status',
            'status_display', 'triggered_by', 'triggered_by_username',
            'campaign', 'asset', 'inputs', 'step_runs', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'organization', 'triggered_by', 'created_at', 'completed_at']
