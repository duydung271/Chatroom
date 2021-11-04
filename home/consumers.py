import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
number_of_users = 0

class HomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'global'
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    
        global number_of_users

        user = self.scope['user']
        if user.is_authenticated:
            number_of_users+=1
            await self.accept()
            await database_sync_to_async(self.update_user_status)(user,"online")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_status_user',
                    'message': user.username,
                }
            )
            

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Leave room group
        global number_of_users
        number_of_users-=1
        user = self.scope['user']
        if user.is_authenticated:
            number_of_users-=1
            await database_sync_to_async(self.update_user_status)(user,"offline")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_status_user',
                    'message': user.username,
                }
            )

    async def update_status_user(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
                'message': {'message-type':'update-status-user', 'message-body':message}
            }))

    
    async def receive(self, text_data):
        received_data = json.loads(text_data)
    
    def update_user_status(self,user,status):
        user.status.status=status
        user.status.save()