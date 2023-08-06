import asyncio
import inspect

from endpointlib.endpoints.endpoint_device import EndpointDevice

class EndpointMonitorDevice(EndpointDevice):
    def __init__(self, host, port, device, delay, command, on_monitor_callback=None, main_callback=None, handlers=None, on_idle_callback=None, idle_delay=1):
        super().__init__(host, port, device=device, main_callback=main_callback, handlers=handlers, on_idle_callback=on_idle_callback, idle_delay=idle_delay)
        self._delay = delay
        self._command = command
        self._on_monitor = on_monitor_callback

    async def run_monitor(self, on_tasks_ready):
        await on_tasks_ready.wait()
        while True:
            status = await self.send_to_device(self._command)
            try:
                # If callback defined then runit else run on_monitor for inheritors
                if self._on_monitor:
                    if inspect.iscoroutinefunction(self._on_monitor):
                        params = len(inspect.signature(self._on_monitor).parameters)
                        if (params == 1):
                            await self._on_monitor(status)
                    else:
                        await asyncio.get_event_loop().run_in_executor(None, self._on_monitor, status)
                else:
                    await self.on_monitor(status)
            except Exception as ex:
                await self.get_logger().error(str(ex))

            await asyncio.sleep(delay=self._delay)

    async def on_monitor(self, status):
        pass

    def get_tasks_started_by(self, on_tasks_ready):
        tasks = super().get_tasks_started_by(on_tasks_ready)
        tasks.append(self.run_monitor(on_tasks_ready))
        return tasks
