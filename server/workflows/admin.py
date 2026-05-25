from django.contrib import admin
from .models import WorkflowTemplate, WorkflowStep, WorkflowInstance, StepExecution


class WorkflowStepInline(admin.TabularInline):
    model = WorkflowStep
    extra = 0
    ordering = ['order']


@admin.register(WorkflowTemplate)
class WorkflowTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'is_active', 'created_at']
    list_filter = ['is_active', 'organization']
    inlines = [WorkflowStepInline]


@admin.register(WorkflowInstance)
class WorkflowInstanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'template', 'status', 'current_step', 'started_at']
    list_filter = ['status', 'organization']


@admin.register(StepExecution)
class StepExecutionAdmin(admin.ModelAdmin):
    list_display = ['instance', 'step', 'assigned_to', 'status', 'started_at']
    list_filter = ['status']
