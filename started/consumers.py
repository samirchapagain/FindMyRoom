import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message, ClientPayment

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Check if user has access to this room
        has_access = await self.check_room_access()
        if not has_access:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        # amazonq-ignore-next-line
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # amazonq-ignore-next-line
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'chat_message')
        
        if message_type == 'chat_message':
            # amazonq-ignore-next-line
            message = text_data_json['message']
            receiver_id = text_data_json.get('receiver_id')
            
            # Save message to database
            saved_message = await self.save_message(message, receiver_id)
            
            if saved_message:
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': saved_message
                    }
                )
    
    async def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))
    
    @database_sync_to_async
    def check_room_access(self):
        try:
            room = Room.objects.get(id=self.room_id)
            
            # Check if user is client with access or room owner
            if hasattr(self.user, 'client'):
                return ClientPayment.objects.filter(
                    client=self.user.client,
                    room=room,
                    status='success'
                ).exists()
            elif hasattr(self.user, 'owner'):
                return room.owner == self.user.owner
            
            return False
        # amazonq-ignore-next-line
        except Room.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, content, receiver_id):
        try:
            room = Room.objects.get(id=self.room_id)
            
            # Determine receiver
            if hasattr(self.user, 'client'):
                receiver = room.owner.user
            elif hasattr(self.user, 'owner'):
                # amazonq-ignore-next-line
                receiver = User.objects.get(id=receiver_id)
            else:
                return None
            
            message = Message.objects.create(
                sender=self.user,
                receiver=receiver,
                room=room,
                content=content
            )
            
            return {
                'id': message.id,
                'content': message.content,
                'sender_id': message.sender.id,
                'sender_name': message.sender.username,
                'receiver_id': message.receiver.id,
                'timestamp': message.timestamp.isoformat(),
                'is_mine': True
            }
        except Exception as e:
            # amazonq-ignore-next-line
            print(f"Error saving message: {e}")
            return None

class PaymentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Join user-specific group for payment notifications
        # amazonq-ignore-next-line
        self.user_group_name = f'client_{self.user.id}'
        
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave user group
        # amazonq-ignore-next-line
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
    
    async def payment_success(self, event):
        # Send payment success notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'payment_success',
            # amazonq-ignore-next-line
            'room_id': event['room_id'],
            'message': event['message']
        }))