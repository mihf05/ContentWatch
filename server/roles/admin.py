from django.contrib import admin
from .models import Role, ResourcePermission


class ResourcePermissionInline(admin.TabularInline):
    model = ResourcePermission
    extra = 0


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'is_system', 'is_default', 'created_at']
    list_filter = ['is_system', 'is_default', 'organization']
    inlines = [ResourcePermissionInline]


@admin.register(ResourcePermission)
class ResourcePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'resource', 'can_read', 'can_create', 'can_update', 'can_delete']
    list_filter = ['resource', 'role__organization']
