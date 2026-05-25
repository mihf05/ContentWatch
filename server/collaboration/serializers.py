from rest_framework import serializers
from .models import Activity, Comment, Notification, Presence


class ActivitySerializer(serializers.ModelSerializer):
    actor_email = serializers.CharField(source='actor.email', read_only=True, default=None)

    class Meta:
        model = Activity
        fields = [
            'id', 'organization', 'actor', 'actor_email', 'action',
            'resource_type', 'resource_id', 'resource_title',
            'details', 'created_at',
        ]
        read_only_fields = ['__all__']


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.CharField(source='author.email', read_only=True)
    author_name = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'organization', 'author', 'author_email', 'author_name',
            'resource_type', 'resource_id', 'content',
            'parent', 'is_edited', 'is_pinned', 'reply_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['organization', 'author', 'is_edited', 'created_at', 'updated_at']

    def get_author_name(self, obj):
        u = obj.author
        return f"{u.first_name} {u.last_name}".strip() or u.email

    def get_reply_count(self, obj):
        return obj.replies.count()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['resource_type', 'resource_id', 'content', 'parent']


class NotificationSerializer(serializers.ModelSerializer):
    actor_email = serializers.CharField(source='actor.email', read_only=True, default=None)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'organization', 'notification_type',
            'title', 'message', 'resource_type', 'resource_id',
            'actor', 'actor_email', 'is_read', 'read_at', 'created_at',
        ]
        read_only_fields = [
            'recipient', 'organization', 'notification_type',
            'title', 'message', 'resource_type', 'resource_id',
            'actor', 'created_at',
        ]


class PresenceSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Presence
        fields = [
            'user', 'user_email', 'user_name',
            'status', 'current_resource_type', 'current_resource_id',
            'last_seen',
        ]

    def get_user_name(self, obj):
        u = obj.user
        return f"{u.first_name} {u.last_name}".strip() or u.email
