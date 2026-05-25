from django.contrib import admin
from .models import MessageThread, ThreadParticipant, Message, MessageReaction


class ThreadParticipantInline(admin.TabularInline):
    model = ThreadParticipant
    extra = 0


@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'thread_type', 'organization', 'is_archived', 'created_at']
    list_filter = ['thread_type', 'is_archived']
    inlines = [ThreadParticipantInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'thread', 'message_type', 'is_edited', 'is_deleted', 'created_at']
    list_filter = ['message_type', 'is_deleted']
