from rest_framework import serializers
from .models import MessageThread, ThreadParticipant, Message, MessageReaction


class MessageReactionSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = MessageReaction
        fields = ['id', 'user', 'user_email', 'emoji', 'created_at']
        read_only_fields = ['user', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    sender_name = serializers.SerializerMethodField()
    reactions = MessageReactionSerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 'thread', 'sender', 'sender_email', 'sender_name',
            'content', 'message_type', 'file', 'file_name', 'file_size',
            'parent', 'is_edited', 'is_deleted', 'edited_at',
            'reactions', 'reply_count', 'created_at',
        ]
        read_only_fields = [
            'thread', 'sender', 'is_edited', 'is_deleted',
            'edited_at', 'created_at',
        ]

    def get_sender_name(self, obj):
        u = obj.sender
        return f"{u.first_name} {u.last_name}".strip() or u.email

    def get_reply_count(self, obj):
        return obj.replies.count()


class MessageCreateSerializer(serializers.Serializer):
    content = serializers.CharField()
    message_type = serializers.ChoiceField(
        choices=Message.MESSAGE_TYPE_CHOICES, default='text',
    )
    file = serializers.FileField(required=False, allow_null=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)


class ThreadParticipantSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    unread_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ThreadParticipant
        fields = [
            'id', 'thread', 'user', 'user_email', 'user_name',
            'role', 'last_read_at', 'is_muted', 'unread_count', 'joined_at',
        ]
        read_only_fields = ['thread', 'user', 'joined_at']

    def get_user_name(self, obj):
        u = obj.user
        return f"{u.first_name} {u.last_name}".strip() or u.email


class MessageThreadSerializer(serializers.ModelSerializer):
    participants = ThreadParticipantSerializer(many=True, read_only=True)
    last_message = MessageSerializer(read_only=True)
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = MessageThread
        fields = [
            'id', 'organization', 'title', 'thread_type', 'campaign',
            'is_archived', 'participants', 'last_message', 'unread_count',
            'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['organization', 'created_by', 'created_at', 'updated_at']

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 0
        try:
            participant = obj.participants.get(user=request.user)
            return participant.unread_count
        except ThreadParticipant.DoesNotExist:
            return 0


class MessageThreadListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing threads."""
    last_message_preview = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = MessageThread
        fields = [
            'id', 'title', 'thread_type', 'campaign', 'is_archived',
            'last_message_preview', 'participant_count', 'unread_count',
            'updated_at',
        ]

    def get_last_message_preview(self, obj):
        msg = obj.messages.order_by('-created_at').first()
        if not msg:
            return None
        return {
            'sender': msg.sender.email,
            'content': msg.content[:100] if msg.content else '',
            'created_at': msg.created_at,
        }

    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 0
        try:
            participant = obj.participants.get(user=request.user)
            return participant.unread_count
        except ThreadParticipant.DoesNotExist:
            return 0


class MessageThreadCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True, default='')
    thread_type = serializers.ChoiceField(
        choices=MessageThread.THREAD_TYPE_CHOICES, default='group',
    )
    campaign_id = serializers.IntegerField(required=False, allow_null=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list,
    )
