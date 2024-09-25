"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from pong.routing import websocket_urlpatterns as pong_websocket_urlpatterns
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from friend.routing import websocket_urlpatterns as friend_websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                pong_websocket_urlpatterns + chat_websocket_urlpatterns + friend_websocket_urlpatterns
            )
        )
    ),
})

