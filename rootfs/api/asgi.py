"""
ASGI config for manager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from .routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.production')
http = get_asgi_application()
websocket = AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(
    websocket_urlpatterns
)))

application = ProtocolTypeRouter({"http": http, "websocket": websocket})
