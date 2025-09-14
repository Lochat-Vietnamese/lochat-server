from django.urls import re_path
from app.consumers.chatConsumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'chat/(?P<id>[0-9a-f\-]+)$', ChatConsumer.as_asgi()),
]