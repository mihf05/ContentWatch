from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'resource_type', 'resource_id', 'actor', 'processed', 'created_at']
    list_filter = ['event_type', 'processed', 'resource_type']
    readonly_fields = ['event_type', 'payload', 'actor', 'resource_type', 'resource_id', 'created_at']
