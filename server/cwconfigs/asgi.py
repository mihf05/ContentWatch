"""
ASGI config for ContentWatch project.
Supports HTTP + WebSocket protocols via Django Channels.
"""

import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cwconfigs.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from collaboration.routing import websocket_urlpatterns as collaboration_ws
from ai_workflows.routing import websocket_urlpatterns as ai_ws

combined_websocket_urlpatterns = collaboration_ws + ai_ws

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(combined_websocket_urlpatterns),
    ),
})
