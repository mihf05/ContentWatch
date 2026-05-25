from django.conf import settings
from django.db import models


class AIAgentProfile(models.Model):
    """
    Profile representing a customized AI Agent that performs specific tasks in the workflow.
    """
    ROLE_CHOICES = [
        ('writer', 'Creative Copywriter / Scriptwriter'),
        ('reviewer', 'Brand Safety / Style Guide Auditor'),
        ('seo', 'SEO & Audience Targeting Expert'),
        ('designer', 'Visual Concept & Thumbnail Strategist'),
    ]

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='ai_agents'
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    system_prompt = models.TextField(
        help_text="Define the expertise, instructions, and rules for this agent."
    )
    temperature = models.FloatField(default=0.7)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['role', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class AIKnowledgeDocument(models.Model):
    """
    Knowledge store for Retrieval-Augmented Generation (RAG). Contains style guides,
    brand voice references, past analytics, and guidelines for context injection.
    """
    CATEGORY_CHOICES = [
        ('brand_voice', 'Brand Voice & Tone'),
        ('style_guide', 'Style & Format Book'),
        ('analytics', 'Audience Analytics & Key Metrics'),
        ('reference', 'General Reference Guidelines'),
    ]

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='ai_knowledge_docs'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Raw guideline document or reference text.")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='brand_voice')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} [{self.get_category_display()}]"


class AIPipelineTemplate(models.Model):
    """
    A blueprint defining a sequential or coordinated AI content generation/optimization pipeline.
    """
    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='ai_pipeline_templates'
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class AIPipelineStep(models.Model):
    """
    A single step within an AI generation pipeline, specifying the agent, prompt, and step type.
    """
    STEP_TYPE_CHOICES = [
        ('script_generation', 'AI Script / Content Generation'),
        ('brand_voice_check', 'AI Brand Voice & Guidelines Auditor'),
        ('thumbnail_concept', 'AI Thumbnail Strategist & Concept Generator'),
        ('seo_optimization', 'AI SEO & Hashtag Optimization'),
    ]

    template = models.ForeignKey(
        AIPipelineTemplate, on_delete=models.CASCADE, related_name='steps'
    )
    agent = models.ForeignKey(
        AIAgentProfile, on_delete=models.PROTECT, related_name='pipeline_steps'
    )
    name = models.CharField(max_length=150)
    step_type = models.CharField(max_length=40, choices=STEP_TYPE_CHOICES)
    order = models.PositiveIntegerField()
    prompt_template = models.TextField(
        help_text="Prompt instructions with optional placeholders like {topic}, {audience}."
    )

    class Meta:
        ordering = ['order']
        unique_together = ['template', 'order']

    def __str__(self):
        return f"{self.template.name} - #{self.order} {self.name}"


class AIPipelineRun(models.Model):
    """
    A single execution instance of an AI pipeline.
    """
    STATUS_CHOICES = [
        ('idle', 'Idle / Draft'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    organization = models.ForeignKey(
        'teams.Organization', on_delete=models.CASCADE, related_name='ai_pipeline_runs'
    )
    template = models.ForeignKey(
        AIPipelineTemplate, on_delete=models.CASCADE, related_name='runs'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idle')
    triggered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    campaign = models.ForeignKey(
        'campaigns.Campaign', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_runs'
    )
    asset = models.ForeignKey(
        'assets.Asset', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_runs'
    )
    inputs = models.JSONField(
        default=dict, blank=True,
        help_text="Execution inputs e.g. {'topic': '...', 'audience': '...'}"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.template.name} Run #{self.id} ({self.get_status_display()})"


class AIStepRun(models.Model):
    """
    Execution run of a single step inside an AI pipeline run, logging agent thoughts and outputs.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    pipeline_run = models.ForeignKey(
        AIPipelineRun, on_delete=models.CASCADE, related_name='step_runs'
    )
    step = models.ForeignKey(
        AIPipelineStep, on_delete=models.CASCADE, related_name='step_runs'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    agent_thoughts = models.TextField(
        blank=True,
        help_text="Detailed trace logs of the agent's thought process, steps, and intermediate decisions."
    )
    output_content = models.TextField(
        blank=True,
        help_text="Markdown output produced by the agent step."
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['step__order']

    def __str__(self):
        return f"Run #{self.pipeline_run.id} - Step: {self.step.name} ({self.get_status_display()})"
