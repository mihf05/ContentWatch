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

from collaboration.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns),
    ),
})
