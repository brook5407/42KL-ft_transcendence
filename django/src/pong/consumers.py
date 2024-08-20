# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class PongConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 'test'

		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		self.accept()
		
		# self.send(text_data=json.dumps({
		# 	'type':'connection_established',
		# 	'message':'You are now connected!'
		# }))

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type':'chat_message',
				'message':message
			}
		)
		# print('Message:', message)

		# self.send(text_data=json.dumps({
		# 	'type':'chat',
		# 	'message':message
		# }))

	def chat_message(self, event):
		message = event['message']

		self.send(text_data=json.dumps({
			'type':'chat',
			'message':message
		}))

# class PongConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'pong_{self.room_name}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#         # Assign the paddle to the player based on the number of connections
#         if not hasattr(self.channel_layer, 'players'):
#             self.channel_layer.players = []

#         if len(self.channel_layer.players) < 2:
#             self.player = f'paddle{len(self.channel_layer.players) + 1}'
#             self.channel_layer.players.append(self.player)
#         else:
#             # If more than two players attempt to connect
#             await self.close()

#         # Send paddle assignment to the client
#         await self.send(text_data=json.dumps({
#             'player': self.player
#         }))

#     async def disconnect(self, close_code):
#         # Remove player from the list when they disconnect
#         self.channel_layer.players.remove(self.player)
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         paddle = text_data_json['paddle']
#         velocity = text_data_json['velocity']

#         # Broadcast the paddle movement to the group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'paddle_movement',
#                 'paddle': paddle,
#                 'velocity': velocity
#             }
#         )

#     async def paddle_movement(self, event):
#         paddle = event['paddle']
#         velocity = event['velocity']

#         # Send movement data to WebSocket
#         await self.send(text_data=json.dumps({
#             'paddle': paddle,
#             'velocity': velocity
#         }))
