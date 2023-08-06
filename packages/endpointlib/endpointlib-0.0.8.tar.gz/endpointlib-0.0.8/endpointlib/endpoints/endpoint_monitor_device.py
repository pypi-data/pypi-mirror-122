import asyncio
import inspect

from asyncio_mqtt import client

from endpointlib.clients.mqtt_async_client import MQTTAsyncClient
from endpointlib.endpoints.endpoint_device import EndpointDevice

class EndpointMonitorDevice(EndpointDevice):
    def __init__(self, host, port, device, monitor_device, delay, command, on_monitor_callback=None, main_callback=None, handlers=None, on_idle_callback=None, idle_delay=1):
        super().__init__(host, port, device=device, main_callback=main_callback, handlers=handlers, on_idle_callback=on_idle_callback, idle_delay=idle_delay)
        self._monitor_device = monitor_device
        self._delay = delay
        self._command = command
        self._on_monitor = on_monitor_callback

    async def run_monitor(self):
        client = self.get_mqtt_client()
        while True:
            status = await self._monitor_device.send_command(self._command)
            try:
                # If callback defined then runit else run on_monitor for inheritors
                if self._on_monitor:
                    if inspect.iscoroutinefunction(self._on_monitor):
                        params = len(inspect.signature(self._on_monitor).parameters)
                        if (params == 2):
                            await self._on_monitor(status, client)
                        elif (params == 3):
                            dev = self.get_device()
                            await self._on_monitor(status, dev, client)
                    else:
                        await asyncio.get_event_loop().run_in_executor(None, self._on_monitor, status)
                else:
                    dev = self.get_device()
                    await self.on_monitor(status, dev, client)
            except Exception as ex:
                await self.get_logger().error(str(ex))

            await asyncio.sleep(delay=self._delay)

    async def on_monitor(self, status, device, client):
        pass

    def get_monitor_device(self):
        return self._monitor_device

    def get_routines(self):
        tasks = super().get_routines()
        tasks.append(self.run_monitor())
        return tasks
