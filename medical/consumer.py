# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # This is where the user connects to the WebSocket
        self.room_name = 'support_chat'
        self.room_group_name = f'chat_{self.room_name}'

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from the group
    async def chat_message(self, event):
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
