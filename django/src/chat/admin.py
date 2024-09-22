from django.contrib import admin
from .models import ChatRoom, ChatMessage, ActiveChatRoom

admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(ActiveChatRoom)