from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from urllib.parse import parse_qs
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
    # Regular expression to match common image file extensions
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']
    pattern2 = r'^(?:data:image/(?:png|jpeg|gif|webp);base64,)'
    pattern1 = r'^https?://.*\.(' + '|'.join(image_extensions) + r')'
    pattern3 = r'^https?://images.*\.(' + '|'+ r')'

    combined_pattern = f"({pattern1})|({pattern3})|({pattern2}.*)"
    
    # Compile the regex pattern
    regex = re.compile(combined_pattern, re.IGNORECASE)
    
    # Check if the URL matches the pattern
    if regex.match(url):
        return True
    else:
        return False

class ChatConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, message):
        self.chat_room = '123'
        # self.chat_room = self.scope['url_route']['kwargs']['room_name']
        
        await self.accept()
        if self.channel_layer is not None:
            await self.channel_layer.group_add(self.chat_room, self.channel_name)
        else:
            print("Channel Layer return None")

    async def websocket_receive(self, message):
        try:
            query_params = parse_qs(self.scope['query_string'].decode())
            self.customer_name = query_params.get('customer_name', ['Anonymous'])[0]

            text_data = json.loads(message['text'])

            if text_data['type'] == 'message':
                if " shabi " in text_data['message'] or "傻逼" in text_data['message']:
                    text_data['message'] = f"服务器:【{self.customer_name}】你才是傻逼 "
                    await self.send_self_chat_message(text_data['message'])
                elif self.check_if_static_image(text_data):
                    return
                elif is_online_image_url(text_data['message']):
                    response = text_data['message']
                    await self.send_image_message(response)
                else:
                    text_data['message'] = text_data['message']
                    await self.send_chat_message(text_data['message'])
            elif text_data['type'] == 'image':
                await self.send_image_message(text_data['image'])

        except json.JSONDecodeError as e:
            error_message = {'type': 'error', 'message': 'Invalid JSON format in received message.'}
            await self.send(json.dumps(error_message))
        except Exception as e:
            error_message = {'type': 'error', 'message': str(e)}
            await self.send(json.dumps(error_message))

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(self.chat_room, self.channel_name)
        raise StopConsumer()

    async def send_chat_message(self, message):
        query_params = parse_qs(self.scope['query_string'].decode())
        self.customer_name = query_params.get('customer_name', ['Anonymous'])[0]
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat.message",
                "name": self.customer_name,
                "message": message
            }
        )

    async def send_self_chat_message(self, message):
        query_params = parse_qs(self.scope['query_string'].decode())
        self.customer_name = query_params.get('customer_name', ['Anonymous'])[0]
        
        # Create a message with image data
        message = {
            "type": "image.message",
            "name": self.customer_name,
            "message": message
        }
        # Send the message directly to the WebSocket channel
        await self.send(text_data=json.dumps(message))



    async def send_image_message(self, image_data):
        query_params = parse_qs(self.scope['query_string'].decode())
        self.customer_name = query_params.get('customer_name', ['Anonymous'])[0]
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "image.message",
                "name": self.customer_name,
                "image": image_data
            }
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