from rest_framework import serializers
from .models import AssetFolder, Asset, AssetVersion, AssetComment


class AssetFolderSerializer(serializers.ModelSerializer):
    path = serializers.CharField(read_only=True)
    asset_count = serializers.SerializerMethodField()
    subfolder_count = serializers.SerializerMethodField()

    class Meta:
        model = AssetFolder
        fields = [
            'id', 'organization', 'name', 'parent', 'color',
            'path', 'asset_count', 'subfolder_count',
            'created_by', 'created_at',
        ]
        read_only_fields = ['organization', 'created_by', 'created_at']

    def get_asset_count(self, obj):
        return obj.assets.count()

    def get_subfolder_count(self, obj):
        return obj.children.count()


class AssetVersionSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.CharField(
        source='uploaded_by.email', read_only=True, default=None,
    )

    class Meta:
        model = AssetVersion
        fields = [
            'id', 'version_number', 'file', 'file_size',
            'changelog', 'uploaded_by', 'uploaded_by_email', 'created_at',
        ]
        read_only_fields = ['version_number', 'uploaded_by', 'created_at']


class AssetCommentSerializer(serializers.ModelSerializer):
    author_email = serializers.CharField(source='author.email', read_only=True)
    author_name = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = AssetComment
        fields = [
            'id', 'asset', 'author', 'author_email', 'author_name',
            'content', 'position_x', 'position_y', 'timestamp_seconds',
            'parent', 'is_resolved', 'is_edited', 'reply_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['asset', 'author', 'is_edited', 'created_at', 'updated_at']

    def get_author_name(self, obj):
        u = obj.author
        return f"{u.first_name} {u.last_name}".strip() or u.email

    def get_reply_count(self, obj):
        return obj.replies.count()


class AssetSerializer(serializers.ModelSerializer):
    versions = AssetVersionSerializer(many=True, read_only=True)
    comments = AssetCommentSerializer(many=True, read_only=True)
    uploaded_by_email = serializers.CharField(
        source='uploaded_by.email', read_only=True, default=None,
    )
    folder_name = serializers.CharField(source='folder.name', read_only=True, default=None)

    class Meta:
        model = Asset
        fields = [
            'id', 'organization', 'folder', 'folder_name',
            'campaign', 'deliverable',
            'name', 'description', 'asset_type', 'file',
            'file_size', 'mime_type', 'status',
            'tags', 'metadata', 'current_version',
            'versions', 'comments',
            'uploaded_by', 'uploaded_by_email', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'organization', 'file_size', 'mime_type', 'current_version',
            'uploaded_by', 'created_at', 'updated_at',
        ]


class AssetListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    uploaded_by_email = serializers.CharField(
        source='uploaded_by.email', read_only=True, default=None,
    )
    folder_name = serializers.CharField(source='folder.name', read_only=True, default=None)

    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'asset_type', 'file', 'file_size',
            'mime_type', 'status', 'tags', 'current_version',
            'folder', 'folder_name',
            'uploaded_by_email', 'created_at',
        ]


class AssetUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            'name', 'description', 'asset_type', 'file',
            'folder', 'campaign', 'deliverable', 'tags', 'metadata',
        ]

    def create(self, validated_data):
        request = self.context['request']
        org_id = self.context['view'].kwargs['org_id']
        file_obj = validated_data.get('file')

        asset = Asset.objects.create(
            organization_id=org_id,
            uploaded_by=request.user,
            file_size=file_obj.size if file_obj else 0,
            mime_type=file_obj.content_type if file_obj else '',
            **validated_data,
        )

        # Create initial version
        if file_obj:
            AssetVersion.objects.create(
                asset=asset,
                version_number=1,
                file=file_obj,
                file_size=file_obj.size,
                changelog='Initial upload',
                uploaded_by=request.user,
            )

        return asset


class AssetNewVersionSerializer(serializers.Serializer):
    file = serializers.FileField()
    changelog = serializers.CharField(required=False, allow_blank=True, default='')
