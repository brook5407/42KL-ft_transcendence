from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from urllib.parse import parse_qs
from chat.models import ChatRoom, ChatMessage
from django.contrib.auth.models import User
import asyncio
import re
import json

TABLE = {
    'dog': '/static/images/meme/9299765.jpg',
    'miku': '/static/images/meme/miku_impatient.png',
    'miku_confused': '/static/images/meme/miku_confused.png',
    'minion': 'https://miro.medium.com/v2/resize:fit:1000/format:webp/1*AmI9wRbXrfIWGESx6eEiTw.gif',
}

def is_online_image_url(url):
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']
    pattern2 = r'^(?:data:image/(?:png|jpeg|gif|webp);base64,)'
    pattern1 = r'^https?://.*\.(' + '|'.join(image_extensions) + r')'
    pattern3 = r'^https?://images.*\.(' + '|'+ r')'

    combined_pattern = f"({pattern1})|({pattern3})|({pattern2}.*)"
    regex = re.compile(combined_pattern, re.IGNORECASE)
    
    if regex.match(url):
        return True
    else:
        return False

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def websocket_connect(self, message):
        self.chat_room = self.scope['url_route']['kwargs']['group_num']
        
        # self.room_id = self.scope['url_route']['kwargs'].get('room_id')
        # self.room = ChatRoom.objects.get(id=self.room_id)
        # self.room_name = self.room.get_room_name(self.scope['user'])
        
        print("self.chat_room: " + self.chat_room)
        self.room_group_name = f'chat_{self.chat_room}'
        
        self.customer_name = self.scope["user"].username
        
        # self.receiver_id = "Name"
        # self.receiver_id = self.scope['url_route']['kwargs'].get('receiver_id', None)
        
        await self.accept()
        if self.channel_layer is not None:
            await self.channel_layer.group_add(self.chat_room, self.channel_name)
        else:
            print("Channel Layer returned None. Cannot join the chat room.")

    async def websocket_receive(self, message):
        try:
            text_data = json.loads(message['text'])
            message_type = text_data.get('type', None)
            message_content = text_data.get('message', None)
            self.receiver_id = text_data.get('receiver_id', None)

            if message_type == 'message' and message_content:
                if " shabi " in message_content or "傻逼" in message_content:
                    message_content = f"服务器:【{self.customer_name}】你才是傻逼 "
                    await self.send_self_chat_message(message_content)
                elif self.check_if_static_image(text_data):
                    return
                elif is_online_image_url(message_content):
                    await self.send_image_message(message_content)
                else:
                    await self.send_chat_message(message_content)
            elif message_type == 'image' and 'image' in text_data:
                await self.send_image_message(text_data['image'])
            else:
                raise ValueError("Invalid message type or missing content")

        except json.JSONDecodeError as e:
            error_message = {'type': 'error', 'message': 'Invalid JSON format in received message.'}
            await self.send(json.dumps(error_message))
        except Exception as e:
            error_message = {'type': 'error', 'message': str(e)}
            await self.send(json.dumps(error_message))

    async def websocket_disconnect(self, message):
        if self.channel_layer is not None:
            await self.channel_layer.group_discard(self.chat_room, self.channel_name)
        raise StopConsumer()

    async def send_chat_message(self, message):
        query_params = parse_qs(self.scope['query_string'].decode())
        self.customer_name = query_params.get('customer_name', ['Anonymous'])[0]
        
        await self.save_message(message, message_type='text')
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat.message",
                "name": self.customer_name,
                "message": message
            }
        )

    async def send_image_message(self, image_data):
        query_params = parse_qs(self.scope['query_string'].decode())
        self.customer_name = query_params.get('customer_name', ['Anonymous'])[0]
        
        await self.save_message(image_data, message_type='image')
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "image.message",
                "name": self.customer_name,
                "image": image_data
            }
        )

    async def send_self_chat_message(self, message):
        query_params = parse_qs(self.scope['query_string'].decode())
        self.customer_name = query_params.get('customer_name', ['Anonymous'])[0]

        message = {
            "type": "chat.message",
            "name": self.customer_name,
            "message": message
        }
        await self.send(text_data=json.dumps(message))

    async def save_message(self, content, message_type='text'):
        user = self.scope["user"]
        room = await sync_to_async(ChatRoom.objects.get)(name=self.chat_room)
        # self.receiver_id = self.receiver_id[0] if self.receiver_id else None
        
        receiver = None
        if self.receiver_id:
            try:
                receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
            except User.DoesNotExist:
                receiver = None  # Handle case where receiver_id is invalid

        await sync_to_async(ChatMessage.objects.create)(
            sender=user,
            receiver=receiver,
            message=content,
            room=room
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'name': event['name'],
            'message': event['message']
        }))

    async def image_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'image',
            'name': event['name'],
            'image': event['image']
        }))

    def check_if_static_image(self, text_data):
        pattern = r'^:'  # Regex pattern to match ':=' exactly
        if re.match(pattern, text_data['message']):
            response = TABLE.get(text_data['message'][1:], None)
            if response:
                asyncio.create_task(self.send_image_message(response))
            return True
        else:
            return False
