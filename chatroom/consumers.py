from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Room, Message
from django.core import serializers

number_of_users = 0

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global number_of_users
        number_of_users+=1
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        global number_of_users
        number_of_users-=1

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # Update online users
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_online_users',
                'message': number_of_users
            }
        )
        
    async def receive(self, text_data):
        received_data = json.loads(text_data)
        global number_of_users

        if received_data['message'] == 'get-room-messages' and len(received_data)==1:
            room_messages = await database_sync_to_async(self.get_messages)()
            await self.send(text_data=json.dumps({
                'message': {'message-type':'get-room-messages', 'message-body': room_messages}
            }))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_online_users',
                    'message': number_of_users
                }
            )
        else:    
            await database_sync_to_async(self.save_messages)(received_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': received_data,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': {'message-type':'send-group-message', 'message-body':message}
        }))
    # Receive message from room group
    async def update_online_users(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': {'message-type':'update-online-users', 'message-body':message}
        }))

    def get_messages(self):
        try:
        # if room exists get messages
            room = Room.objects.get(room_name=self.room_name)
            messages = room.message_set.all()
            data = serializers.serialize("json", messages)
            return data
        except:
        # room doesnt exist, create room
            Room.objects.create(room_name=self.room_name)
        return []

    def save_messages(self,received_data):
        data = received_data
        room = Room.objects.get(room_name=self.room_name)
        Message.objects.create(message=data['message'],sender=data['sender'],room_name=room)