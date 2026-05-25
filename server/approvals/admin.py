from django.contrib import admin
from .models import ApprovalChain, ApprovalLevel, ApprovalRequest, ApprovalDecision


class ApprovalLevelInline(admin.TabularInline):
    model = ApprovalLevel
    extra = 0
    ordering = ['order']


@admin.register(ApprovalChain)
class ApprovalChainAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'resource_type', 'is_active']
    list_filter = ['resource_type', 'is_active']
    inlines = [ApprovalLevelInline]


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'resource_title', 'chain', 'status', 'priority', 'requested_by', 'created_at']
    list_filter = ['status', 'priority']


@admin.register(ApprovalDecision)
class ApprovalDecisionAdmin(admin.ModelAdmin):
    list_display = ['request', 'level', 'approver', 'decision', 'decided_at']
    list_filter = ['decision']
