from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

from core.settings import TIME_ZONE
from .models import Room, Message
from django.core import serializers
from django.contrib.auth.models import User


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

   

    async def receive(self, text_data):
        received_data = json.loads(text_data)
        global number_of_users

        if received_data['message'] == 'get-room-messages' and len(received_data)==1:
            room_messages = await database_sync_to_async(self.get_messages)()
            room_users = await database_sync_to_async(self.get_users)()

            await self.send(text_data=json.dumps({
                'message': {'message-type':'get-room-messages', 'message-body': room_messages}
            }))

            await self.send(text_data=json.dumps({
                'message': {'message-type':'get-room-users', 'message-body': room_users}
            }))

         
        else:    
            data_mess_filter=await database_sync_to_async(self.save_messages)(received_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data_mess_filter,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': {'message-type':'send-group-message', 'message-body':message}
        }))

    def get_messages(self):
        try:
        # if room exists get messages
            room = Room.objects.get(room_name=self.room_name)
            messages = room.message_set.all()
            data_filter=[]
            for message in messages:
                mess_data ={'message': message.message,
                    'sender': message.sender.username,
                    'avatar': message.sender.profile.avatar.url,
                    'time_sent': message.date_sent.strftime("%H:%M")
                }
                data_filter.append(mess_data)
            # data = serializers.serialize("json", messages)
            # print(data)
            # print(data_filter)
            return data_filter
        except:
        # # room doesnt exist, create room
            Room.objects.create(room_name=self.room_name)
            pass
        return []

    def get_users(self):
        try:
        # if room exists get messages
            room = Room.objects.get(room_name=self.room_name)
            user_names = room.get_list_user_names()
            data_filter=[]
            for user_name in user_names:
                try:
                    User.objects.get(username=user_name)
                    mess_data ={'username': user_name,
                    }
                    data_filter.append(mess_data)
                except:
                    pass
            return data_filter
        except:
            return []

    def save_messages(self,received_data):
        data = received_data
        room = Room.objects.get(room_name=self.room_name)
        message=Message.objects.create(message=data['message'],sender=User.objects.get(username=data['sender']),room_name=room)
        return  {'message': message.message,
                    'sender': message.sender.username,
                    'avatar': message.sender.profile.avatar.url,
                    'time_sent': message.date_sent.strftime("%H:%M")
                }