from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

thread_router = DefaultRouter()
thread_router.register(r'threads', views.MessageThreadViewSet, basename='thread')

message_router = DefaultRouter()
message_router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('organizations/<int:org_id>/', include(thread_router.urls)),
    path('organizations/<int:org_id>/threads/<int:thread_id>/', include(message_router.urls)),
]
