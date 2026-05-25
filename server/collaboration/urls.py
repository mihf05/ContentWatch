from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

activity_router = DefaultRouter()
activity_router.register(r'activities', views.ActivityViewSet, basename='activity')

comment_router = DefaultRouter()
comment_router.register(r'comments', views.CommentViewSet, basename='comment')

presence_router = DefaultRouter()
presence_router.register(r'presence', views.PresenceViewSet, basename='presence')

notification_router = DefaultRouter()
notification_router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('organizations/<int:org_id>/', include(activity_router.urls)),
    path('organizations/<int:org_id>/', include(comment_router.urls)),
    path('organizations/<int:org_id>/', include(presence_router.urls)),
    path('', include(notification_router.urls)),
]
