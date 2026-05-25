from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ai/run/<int:run_id>/', consumers.AIConsumer.as_asgi()),
]
