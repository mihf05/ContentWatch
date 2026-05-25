from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'chains', views.ApprovalChainViewSet, basename='approval-chain')
router.register(r'requests', views.ApprovalRequestViewSet, basename='approval-request')

urlpatterns = [
    path('organizations/<int:org_id>/approvals/', include(router.urls)),
]
