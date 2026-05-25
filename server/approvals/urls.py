from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

chain_router = DefaultRouter()
chain_router.register(r'chains', views.ApprovalChainViewSet, basename='approval-chain')

request_router = DefaultRouter()
request_router.register(r'requests', views.ApprovalRequestViewSet, basename='approval-request')

urlpatterns = [
    path('organizations/<int:org_id>/approvals/', include(chain_router.urls)),
    path('organizations/<int:org_id>/approvals/', include(request_router.urls)),
]
