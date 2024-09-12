from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from chat.models import ChatRoom, ChatMessage
from django.contrib.auth.models import User
from django.db import transaction
import asyncio
import re
import json

# WXR TODO