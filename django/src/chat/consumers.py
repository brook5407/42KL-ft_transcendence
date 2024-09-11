from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from chat.models import ChatRoom, ChatMessage
from django.contrib.auth.models import User
from django.db import transaction
import asyncio
import re
import json
import logging

logger = logging.getLogger(__name__)

# Static images mapping
TABLE = {
    'dog': '/static/images/meme/9299765.jpg',
    'miku': '/static/images/meme/miku_impatient.png',
    'miku_confused': '/static/images/meme/miku_confused.png',
    'minion': 'https://miro.medium.com/v2/resize:fit:1000/format:webp/1*AmI9wRbXrfIWGESx6eEiTw.gif',
}

# Function to verify if a URL is an online image
def is_online_image_url(url):
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']
    pattern = r'^(https?://.*\.(?:' + '|'.join(image_extensions) + r')|data:image/(?:png|jpeg|gif|webp);base64,)'
    return bool(re.match(pattern, url, re.IGNORECASE))

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def websocket_connect(self, message):
        self.chat_room = self.scope['url_route']['kwargs']['group_num']
        self.room_group_name = f'chat_{self.chat_room}'
        self.customer_name = self.scope["user"].username
        
        # if not await self.does_chat_room_exist(self.chat_room):
        #     # await self.send_json({'type': 'error', 'message': 'Chat room does not exist.'})
        #     await self.close()
        #     return
        
        await self.accept()
        if self.channel_layer:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def websocket_receive(self, message):
        try:
            text_data = json.loads(message['text'])
            message_type = text_data.get('type')
            message_content = text_data.get('message')
            self.receiver_id = text_data.get('receiver_id')

            if message_type == 'message' and message_content:
                if " shabi " in message_content or "傻逼" in message_content:
                    message_content = f"服务器:【{self.customer_name}】你才是傻逼 "
                    await self.send_self_chat_message(message_content)
                elif self.check_if_static_image(text_data):
                    return
                elif is_online_image_url(message_content):
                    await self.send_image_message(message_content)
                else:
                    print(f"Message Content BB: {message_content}")
                    await self.send_chat_message(message_content)
            elif message_type == 'image' and 'image' in text_data:
                await self.send_image_message(text_data['image'])
            else:
                raise ValueError("Invalid message type or missing content")

        except json.JSONDecodeError:
            await self.send_json({'type': 'error1', 'message': 'Invalid JSON format in received message.'})
        except Exception as e:
            await self.send_json({'type': 'error2', 'message': str(e)})

    async def websocket_disconnect(self, message):
        if self.channel_layer:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        raise StopConsumer()

    async def send_chat_message(self, message):
        print(f"Message Content AAGGG: {message}")
        await self.save_message(message, message_type='text')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "name": self.customer_name,
                "message": message
            }
        )

    async def send_image_message(self, image_data):
        await self.save_message(image_data, message_type='image')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "image.message",
                "name": self.customer_name,
                "image": image_data
            }
        )

    async def send_self_chat_message(self, message):
        await self.send_json({
            "type": "chat.message",
            "name": self.customer_name,
            "message": message
        })

    # async def save_message(self, content, message_type='text'):
    #     user = self.scope["user"]
    #     try:
    #         room = await sync_to_async(ChatRoom.objects.get)(name=self.chat_room)
    #         receiver = None

    #         if self.receiver_id:
    #             try:
    #                 receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
    #             except User.DoesNotExist:
    #                 pass

    #         await sync_to_async(ChatMessage.objects.create)(
    #             sender=user,
    #             receiver=receiver,
    #             message=content,
    #             room=room
    #         )
    #     except ChatRoom.DoesNotExist:
    #         pass
    
    
# ----------------- Original Code -----------------
    # async def save_message(self, content, message_type='text'):
    #     user = self.scope["user"]
    #     try:
    #         # Use a transaction to ensure atomicity
    #         async with sync_to_async(transaction.atomic):
    #             # Try to fetch the existing chat room
    #             room, created = await sync_to_async(ChatRoom.objects.get_or_create)(name=self.chat_room)
                
    #             # If the room was created, print a debug message
    #             if created:
    #                 print(f"ChatRoom with name {self.chat_room} was created.")
                
    #             # Try to fetch the receiver user if receiver_id is provided
    #             receiver = None
    #             if self.receiver_id:
    #                 try:
    #                     receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
    #                 except User.DoesNotExist:
    #                     receiver = None  # Handle invalid receiver_id

    #             # Save the message in the chat room
    #             await sync_to_async(ChatMessage.objects.create)(
    #                 sender=user,
    #                 receiver=receiver,
    #                 message=content,
    #                 room=room
    #             )
    #     except Exception as e:
    #         print(f"Error saving message: {str(e)}")
# ------------------------------------------------------------------------------------------------------------------------------------
    # async def save_message(self, content, message_type='text'):
    #     user = self.scope["user"]
    #     room_name = ChatRoom.get_private_chat_roomname(user, self.chat_room)
    #     try:
    #         room = await sync_to_async(ChatRoom.objects.get)(name=room_name)
    #     except ChatRoom.DoesNotExist:
    #         room = None

    #     receiver = None

    #     if self.receiver_id:
    #         try:
    #             receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
    #         except User.DoesNotExist:
    #             receiver = None
    #     print(f"Receiver check AAAA: {receiver}")
    #     if room:
    #         await sync_to_async(ChatMessage.objects.create)(
    #             sender=user,
    #             receiver=receiver,
    #             message=content,
    #             room=room
    #         )
    #     print(f"Room check BBBBB: {room}")
    
    
    async def save_message(self, content, message_type='text'):
        user = self.scope["user"]
        print(f"user check XXXX: {self.chat_room}")
        try:
            room_name = sorted([str(user), str(self.chat_room)])
            room_name_join = "-".join(room_name)
            print(f"room_name check ZZZZ: {room_name}")
            room = await sync_to_async(ChatRoom.objects.get)(name=room_name_join)
        except ChatRoom.DoesNotExist:
            print(f"except ChatRoom.DoesNotExist: check YYYY: {room_name}")
            room = None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            print(f"except ChatRoom.DoesNotExist: check YYYY: {str(e)}")
            room = None
        print(f"room check AAAA: {room}")
        receiver = None

        if self.receiver_id:
            try:
                receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
            except User.DoesNotExist:
                receiver = None
        print(f"Receiver check BBBB: {receiver}")
        if room:
            await sync_to_async(ChatMessage.objects.create)(
                sender=user,
                receiver=receiver,
                message=content,
                room=room
            )
# ------------------------------------------------------------------------------------------------------------------------------------
    
    # async def save_message(self, content, message_type='text'):
    #     user = self.scope["user"]
    #     print(f"check room NNNN: {self.chat_room}")
    #     room = await sync_to_async(ChatRoom.objects.get)(name=self.chat_room)
    #     print(f"check room MMM: {self.chat_room}")
    #     # self.receiver_id = self.receiver_id[0] if self.receiver_id else None
        
    #     receiver = None
    #     # print(f"Receiver check AAAA: {receiver}")
    #     if self.receiver_id:
    #         try:
    #             receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
    #             print(f"Receiver ID: {self.receiver_id}")
    #         except User.DoesNotExist:
    #             print(f"User with id {self.receiver_id} does not exist.")
    #             receiver = None  # Handle case where receiver_id is invalid
    #     print(f"Receiver check BBBBB: {receiver}")
    #     await sync_to_async(ChatMessage.objects.create)(
    #         sender=user,
    #         receiver=receiver,
    #         message=content,
    #         room=room
    #     )
    
    async def chat_message(self, event):
        await self.send_json({
            'type': 'message',
            'name': event['name'],
            'message': event['message']
        })

    async def image_message(self, event):
        await self.send_json({
            'type': 'image',
            'name': event['name'],
            'image': event['image']
        })

    def check_if_static_image(self, text_data):
        message = text_data.get('message', '')
        if message.startswith(':'):
            image_path = TABLE.get(message[1:], None)
            if image_path:
                asyncio.create_task(self.send_image_message(image_path))
                return True
        return False

    async def does_chat_room_exist(self, room_name):
        return await sync_to_async(ChatRoom.objects.filter(name=room_name).exists)()

    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))
