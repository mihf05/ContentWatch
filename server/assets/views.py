from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from roles.permissions import HasResourcePermission
from .models import AssetFolder, Asset, AssetVersion, AssetComment
from .serializers import (
    AssetFolderSerializer,
    AssetSerializer, AssetListSerializer, AssetUploadSerializer, AssetNewVersionSerializer,
    AssetVersionSerializer, AssetCommentSerializer,
)


class AssetFolderViewSet(viewsets.ModelViewSet):
    """CRUD for asset folders."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = AssetFolderSerializer
    rbac_resource = 'assets'

    def get_queryset(self):
        qs = AssetFolder.objects.filter(
            organization_id=self.kwargs['org_id'],
        )
        # Filter by parent (null = root folders)
        parent = self.request.query_params.get('parent')
        if parent == 'root':
            qs = qs.filter(parent__isnull=True)
        elif parent:
            qs = qs.filter(parent_id=parent)
        return qs

    def perform_create(self, serializer):
        serializer.save(
            organization_id=self.kwargs['org_id'],
            created_by=self.request.user,
        )

    @action(detail=True, methods=['get'])
    def tree(self, request, org_id=None, pk=None):
        """Get the full subtree of a folder."""
        folder = self.get_object()

        def build_tree(f):
            return {
                'id': f.id,
                'name': f.name,
                'color': f.color,
                'children': [build_tree(child) for child in f.children.all()],
                'asset_count': f.assets.count(),
            }

        return Response(build_tree(folder))


class AssetViewSet(viewsets.ModelViewSet):
    """CRUD for digital assets with versioning."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    rbac_resource = 'assets'

    def get_queryset(self):
        qs = Asset.objects.filter(
            organization_id=self.kwargs['org_id'],
        ).select_related('folder', 'uploaded_by')

        # Filters
        asset_type = self.request.query_params.get('type')
        if asset_type:
            qs = qs.filter(asset_type=asset_type)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        folder = self.request.query_params.get('folder')
        if folder:
            qs = qs.filter(folder_id=folder)

        campaign = self.request.query_params.get('campaign')
        if campaign:
            qs = qs.filter(campaign_id=campaign)

        tag = self.request.query_params.get('tag')
        if tag:
            qs = qs.filter(tags__contains=[tag])

        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return AssetListSerializer
        if self.action == 'create':
            return AssetUploadSerializer
        return AssetSerializer

    @action(detail=True, methods=['post'], parser_classes=[parsers.MultiPartParser])
    def upload_version(self, request, org_id=None, pk=None):
        """Upload a new version of an asset."""
        asset = self.get_object()
        serializer = AssetNewVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_obj = serializer.validated_data['file']
        new_version_number = asset.current_version + 1

        version = AssetVersion.objects.create(
            asset=asset,
            version_number=new_version_number,
            file=file_obj,
            file_size=file_obj.size,
            changelog=serializer.validated_data.get('changelog', ''),
            uploaded_by=request.user,
        )

        # Update the asset's current version and file
        asset.current_version = new_version_number
        asset.file = file_obj
        asset.file_size = file_obj.size
        asset.mime_type = file_obj.content_type or ''
        asset.save(update_fields=['current_version', 'file', 'file_size', 'mime_type'])

        return Response(AssetVersionSerializer(version).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def versions(self, request, org_id=None, pk=None):
        """List all versions of an asset."""
        asset = self.get_object()
        versions = asset.versions.all()
        return Response(AssetVersionSerializer(versions, many=True).data)

    @action(detail=True, methods=['post'])
    def approve(self, request, org_id=None, pk=None):
        """Quick-approve an asset."""
        asset = self.get_object()
        asset.status = 'approved'
        asset.save(update_fields=['status'])
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'])
    def archive(self, request, org_id=None, pk=None):
        """Archive an asset."""
        asset = self.get_object()
        asset.status = 'archived'
        asset.save(update_fields=['status'])
        return Response({'status': 'archived'})


class AssetCommentViewSet(viewsets.ModelViewSet):
    """Comments on an asset (with spatial annotation support)."""

    permission_classes = [IsAuthenticated, HasResourcePermission]
    serializer_class = AssetCommentSerializer
    rbac_resource = 'assets'

    def get_queryset(self):
        return AssetComment.objects.filter(
            asset_id=self.kwargs['asset_id'],
            asset__organization_id=self.kwargs['org_id'],
        ).select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            asset_id=self.kwargs['asset_id'],
            author=self.request.user,
        )

    @action(detail=True, methods=['post'])
    def resolve(self, request, org_id=None, asset_id=None, pk=None):
        comment = self.get_object()
        comment.is_resolved = True
        comment.save(update_fields=['is_resolved'])
        return Response({'status': 'resolved'})

    @action(detail=True, methods=['post'])
    def unresolve(self, request, org_id=None, asset_id=None, pk=None):
        comment = self.get_object()
        comment.is_resolved = False
        comment.save(update_fields=['is_resolved'])
        return Response({'status': 'unresolved'})
