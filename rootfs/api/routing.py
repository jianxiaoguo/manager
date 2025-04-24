# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r'^v1/clusters/(?P<uuid>([\w-]*))/apps/(?P<app>([\w-]*))/terminal/?$',
        consumers.AppTerminalConsumer.as_asgi()),
]
