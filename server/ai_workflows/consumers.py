import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AIConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer that handles real-time streams of AI thoughts,
    output content, and collaborative comments for a specific pipeline run.
    """

    async def connect(self):
        # Read parameters from url routing
        self.run_id = self.scope['url_route']['kwargs']['run_id']
        self.group_name = f"ai_run_{self.run_id}"

        # Join the channel group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        """
        Processes client messages, such as sending manual guidance, comments,
        or feedback to the multi-agent system mid-run.
        """
        action = content.get("action")
        data = content.get("data", {})

        if action == "send_guidance":
            # Broadcast the user's guidance or critique to the entire team (Real-time AI collaboration)
            user = self.scope.get("user")
            username = user.username if user and hasattr(user, 'username') else "Team Member"
            
            from django.utils import timezone
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "ai_message",
                    "message": {
                        "event": "guidance_received",
                        "data": {
                            "user": username,
                            "guidance": data.get("guidance", ""),
                            "timestamp": timezone.now().isoformat()
                        }
                    }
                }
            )

    async def ai_message(self, event):
        """
        Standard handler that passes Celery task progress events (thoughts, chunks, state)
        directly to the WebSocket client.
        """
        await self.send_json(event["message"])
