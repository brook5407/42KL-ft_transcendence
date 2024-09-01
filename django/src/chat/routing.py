from django.urls import re_path, path
from .views import SendMessageAPIView, ChatHistoryAPIView
# from base import consumers
from chat import consumers

#前面的是路由，后面的是处理函数
websocket_urlpatterns = [
    # xxx/room/x1
	re_path(r'room/(?P<group_num>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # path('send_message/<int:receiver_id>', SendMessageAPIView.as_view(), name='chat.send_message'),
    # path('chat_history/<int:receiver_id>', ChatHistoryAPIView.as_view(), name='chat.chat_history'),
	# re_path(r'ws/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi()),
] # something similar to urlpatterns in urls.py

# base(app)/consumers.py need to be created