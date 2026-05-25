from django.contrib import admin
from .models import Campaign, CampaignStage, CampaignDeliverable


class CampaignStageInline(admin.TabularInline):
    model = CampaignStage
    extra = 0
    ordering = ['order']


class CampaignDeliverableInline(admin.TabularInline):
    model = CampaignDeliverable
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'status', 'priority', 'start_date', 'end_date']
    list_filter = ['status', 'priority', 'organization']
    search_fields = ['name']
    inlines = [CampaignStageInline, CampaignDeliverableInline]


@admin.register(CampaignStage)
class CampaignStageAdmin(admin.ModelAdmin):
    list_display = ['name', 'campaign', 'order', 'status', 'due_date']
    list_filter = ['status']


@admin.register(CampaignDeliverable)
class CampaignDeliverableAdmin(admin.ModelAdmin):
    list_display = ['title', 'campaign', 'platform', 'content_type', 'status', 'due_date']
    list_filter = ['status', 'platform', 'content_type']
