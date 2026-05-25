from django.contrib import admin
from .models import Organization, Team, Membership, Invitation, AgencyPartnership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'org_type', 'owner', 'is_active', 'created_at']
    list_filter = ['org_type', 'is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'created_at']
    list_filter = ['organization']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'team', 'is_active', 'joined_at']
    list_filter = ['is_active', 'organization']
    raw_id_fields = ['user', 'organization', 'role', 'team']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'organization', 'role', 'status', 'created_at', 'expires_at']
    list_filter = ['status', 'organization']


@admin.register(AgencyPartnership)
class AgencyPartnershipAdmin(admin.ModelAdmin):
    list_display = ['agency', 'partner', 'status', 'created_at']
    list_filter = ['status']
