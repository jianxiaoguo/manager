import six
import time
import ssl
import logging
import asyncio

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from kubernetes.client import exceptions
from kubernetes.stream.ws_client import STDOUT_CHANNEL, STDERR_CHANNEL, ERROR_CHANNEL
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

from .xterm import Xterm


logger = logging.getLogger(__name__)


class BaseAppConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope["user"] is None:
            raise DenyConnection("User not logged in, session banned")
        await self.accept()


class AppTerminalConsumer(BaseAppConsumer):

    async def mkxterm(self):
        from .utils import get_oauth_token
        from .models.cluster import Cluster
        user = self.scope["user"]
        token = await sync_to_async(get_oauth_token)(user)
        app_id = self.scope["url_route"]["kwargs"]["app"]
        cluster = await sync_to_async(get_object_or_404)(
            Cluster, uuid=self.scope["url_route"]["kwargs"]["uuid"])
        cache_key = f"xterm:{cluster.uuid}-{app_id}"
        xterm = await cache.aget(cache_key)
        if xterm is None:
            xterm = Xterm(app_id, user.username, token, cluster.url)
            await xterm.create()
            await cache.aset(cache_key, xterm, timeout=(settings.XTERM_POD_TIMEOUT - 300))
        elif await xterm.status() not in ["Pending", "Running"]:
            await xterm.clean()
            await xterm.create()
        return xterm

    async def connect(self):
        self.xterm = await self.mkxterm()
        self.stream = None
        while True:
            status = await self.xterm.status()
            if status == "Running":
                self.stream = await self.xterm.stream()
                asyncio.create_task(self.task())
                break
            await asyncio.sleep(2)
        await super().connect()
        self.conneted = True

    async def send(self, data, channel=STDOUT_CHANNEL):
        channel_prefix = chr(channel)
        if data is None:
            return
        elif isinstance(data, bytes):
            channel_prefix = six.binary_type(channel_prefix, "ascii")
            await super().send(bytes_data=channel_prefix+data)
        elif isinstance(data, str):
            await super().send(text_data=channel_prefix+data)

    async def wait(self):
        future, loop = asyncio.Future(), asyncio.get_event_loop()
        loop.add_reader(self.stream.sock, future.set_result, None)

        def one_callback(*args, **kwargs):
            try:
                loop.remove_reader(self.stream.sock)
            except ValueError as e:
                logging.debug(f"Error in remove reader: {e}")

        future.add_done_callback(one_callback)
        await future

    async def task(self):
        try:
            deadline = time.time() + settings.XTERM_POD_TIMEOUT
            while self.stream.is_open() and self.conneted and time.time() < deadline:
                try:
                    await self.wait()
                    self.stream.update()
                    for channel in (ERROR_CHANNEL, STDOUT_CHANNEL, STDERR_CHANNEL):
                        if channel in self.stream._channels:
                            data = self.stream.read_channel(channel)
                            await self.send(data, channel)
                except ssl.SSLEOFError as e:
                    logging.debug(f"ssl eof error: {e}")
        except exceptions.ApiException as e:
            logging.debug(f"api exception: {e}")
            await self.send(str(e), STDERR_CHANNEL)
        finally:
            await self.close(code=1000)

    async def close(self, code=None, reason=None):
        try:
            await super().close(code, reason)
        except Exception as e:
            logging.debug(f"Error in close: {e}")

    async def disconnect(self, close_code):
        if self.stream:
            await sync_to_async(self.stream.close)()
        self.conneted = False
        await self.xterm.clean()

    async def receive(self, text_data=None, bytes_data=None):
        data = text_data if text_data else bytes_data
        channel, data = ord(data[0]), data[1:]
        await sync_to_async(self.stream.write_channel)(channel, data)
