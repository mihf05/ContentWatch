from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet, basename='organization')

# Nested under org
org_router = DefaultRouter()
org_router.register(r'teams', views.TeamViewSet, basename='team')
org_router.register(r'members', views.MembershipViewSet, basename='membership')
org_router.register(r'invitations', views.InvitationViewSet, basename='invitation')
org_router.register(r'partnerships', views.AgencyPartnershipViewSet, basename='partnership')

urlpatterns = [
    path('', include(router.urls)),
    path('organizations/<int:org_id>/', include(org_router.urls)),
]
