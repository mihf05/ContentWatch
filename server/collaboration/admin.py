from django.contrib import admin
from .models import Activity, Comment, Notification, Presence


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['actor', 'action', 'resource_type', 'resource_id', 'organization', 'created_at']
    list_filter = ['action', 'resource_type', 'organization']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'resource_type', 'resource_id', 'is_pinned', 'created_at']
    list_filter = ['resource_type', 'is_pinned']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'organization', 'last_seen']
    list_filter = ['status']
