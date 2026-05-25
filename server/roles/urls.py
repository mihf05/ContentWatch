from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'roles', views.RoleViewSet, basename='role')

urlpatterns = [
    path('organizations/<int:org_id>/', include(router.urls)),
]
