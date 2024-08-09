from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path(r"ws/chat/", ChatConsumer.as_asgi()),
]