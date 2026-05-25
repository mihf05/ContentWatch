from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/org/(?P<org_id>\d+)/$', consumers.OrganizationConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(
        r'ws/org/(?P<org_id>\d+)/threads/(?P<thread_id>\d+)/$',
        consumers.MessagingConsumer.as_asgi(),
    ),
]
