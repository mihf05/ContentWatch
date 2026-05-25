from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

collaboration_router = DefaultRouter()
collaboration_router.register(r'activities', views.ActivityViewSet, basename='activity')
collaboration_router.register(r'comments', views.CommentViewSet, basename='comment')
collaboration_router.register(r'presence', views.PresenceViewSet, basename='presence')

notification_router = DefaultRouter()
notification_router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('organizations/<int:org_id>/', include(collaboration_router.urls)),
    path('', include(notification_router.urls)),
]
