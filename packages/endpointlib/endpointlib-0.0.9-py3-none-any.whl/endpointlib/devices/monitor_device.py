import asyncio
import inspect

from endpointlib.devices.device import Device

class MonitorDevice(Device):
    def __init__(self, connection, command, delay, callback):
        super().__init__(connection)
        self._command = command
        self._delay = delay
        self._callback = callback

    async def run_monitor(self):
        while True:           
            status = await self.send_command(self._command)
            try:
                # If callback defined then runit else run on_monitor for inheritors
                if self._callback:
                    if inspect.iscoroutinefunction(self._callback):
                        await self._callback(status)
                    else:
                        await asyncio.get_event_loop().run_in_executor(None, self._callback(status))
                else:
                    await self.on_monitor(status)
                await asyncio.sleep(delay=self._delay)
            except Exception as ex:
                await self.get_logger().error(str(ex))

    async def on_monitor(self, status):
        pass
