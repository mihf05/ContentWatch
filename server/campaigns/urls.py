from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

campaign_router = DefaultRouter()
campaign_router.register(r'campaigns', views.CampaignViewSet, basename='campaign')

stage_router = DefaultRouter()
stage_router.register(r'stages', views.CampaignStageViewSet, basename='campaign-stage')

deliverable_router = DefaultRouter()
deliverable_router.register(r'deliverables', views.CampaignDeliverableViewSet, basename='campaign-deliverable')

urlpatterns = [
    path('organizations/<int:org_id>/', include(campaign_router.urls)),
    path('organizations/<int:org_id>/campaigns/<int:campaign_id>/', include(stage_router.urls)),
    path('organizations/<int:org_id>/campaigns/<int:campaign_id>/', include(deliverable_router.urls)),
]
