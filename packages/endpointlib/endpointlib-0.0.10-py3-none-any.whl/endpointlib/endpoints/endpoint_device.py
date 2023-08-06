import asyncio
import inspect

from endpointlib.clients.mqtt_async_client import MQTTAsyncClient
from endpointlib.endpoints.endpoint import Endpoint

class EndpointDevice(Endpoint):
    def __init__(self, host, port, device, main_callback=None, handlers=None, on_idle_callback=None, idle_delay=1):
        super().__init__(host, port, main_callback=main_callback, handlers=handlers, on_idle_callback=on_idle_callback, idle_delay=idle_delay)
        self._device = device

    def get_device(self):
        return self._device

    async def send_to_device(self, command):
        return await self._device.send_command(command)

    def setup_process_message(self, client):
        client.process_message = self._process_message_device

    async def _process_message_device(self, topic, payload):
        handler = self.get_command_handlers().get(topic, None)
        if (handler is not None):
            if inspect.iscoroutinefunction(handler):
                params = len(inspect.signature(handler).parameters)
                if (params == 2):
                    await handler(topic, payload)
            else:
                await asyncio.get_event_loop().run_in_executor(None, handler, topic, payload)
