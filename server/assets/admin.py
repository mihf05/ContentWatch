from django.contrib import admin
from .models import AssetFolder, Asset, AssetVersion, AssetComment


@admin.register(AssetFolder)
class AssetFolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'parent', 'created_at']
    list_filter = ['organization']


class AssetVersionInline(admin.TabularInline):
    model = AssetVersion
    extra = 0


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'asset_type', 'status', 'current_version', 'organization', 'created_at']
    list_filter = ['asset_type', 'status', 'organization']
    search_fields = ['name']
    inlines = [AssetVersionInline]


@admin.register(AssetComment)
class AssetCommentAdmin(admin.ModelAdmin):
    list_display = ['asset', 'author', 'is_resolved', 'created_at']
    list_filter = ['is_resolved']
