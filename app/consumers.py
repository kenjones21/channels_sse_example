from channels.generic.http import AsyncHttpConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
import time
import asyncio

class ServerSentEventsConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        print('handlin')
        self.room_name = 'room'
        self.room_group_name = 'chat_%s' % self.room_name

        await self.send_headers(headers=[
            (b"Cache-Control", b"no-cache"),
            (b"Content-Type", b"text/event-stream"),
            (b"Transfer-Encoding", b"chunked"),
        ])
        await self.send_body("event: e\ndata: data goes here\n\n".encode('utf-8'), more_body=True)

        print('group add')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        while True:
            print('group send')
            await asyncio.sleep(5)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': 'hi'
                }
            )

    async def disconnect(self):
        print('disocnnectin')
        # Leave room group

    async def chat_message(self, event):
        print('chat_message')
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'room'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print('we out here')
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
