from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

organization_router = DefaultRouter()
organization_router.register(r'folders', views.AssetFolderViewSet, basename='asset-folder')
organization_router.register(r'assets', views.AssetViewSet, basename='asset')

comment_router = DefaultRouter()
comment_router.register(r'comments', views.AssetCommentViewSet, basename='asset-comment')

urlpatterns = [
    path('organizations/<int:org_id>/', include(organization_router.urls)),
    path('organizations/<int:org_id>/assets/<int:asset_id>/', include(comment_router.urls)),
]
