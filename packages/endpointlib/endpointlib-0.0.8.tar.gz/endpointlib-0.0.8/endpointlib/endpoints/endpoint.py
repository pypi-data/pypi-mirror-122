import asyncio
import inspect
import uuid

from asyncio_mqtt import client

from endpointlib.clients.mqtt_async_client import MQTTAsyncClient
from endpointlib.helpers.loggers.logger_manager import LoggerManager

class Endpoint:
    def __init__(self, host, port, main_callback=None, handlers=None, on_idle_callback=None, idle_delay=1):
        if (handlers is None):
            handlers = dict()
        self.id = str(uuid.uuid4())
        self.host = host
        self.port = port
        self._main_callback = main_callback
        self._handlers = handlers
        self._on_idle = on_idle_callback
        self._idle_delay = idle_delay
        self._command_handlers = dict()
        self._mqtt_client = None
        self._logger = LoggerManager.get_async_logger(name='endpointlib')

    def get_id(self):
        return self._id
    
    def get_logger(self):
        return self._logger

    def create_id(self):
        return str(uuid.uuid4())

    async def run_forever(self):
        try:
            tasks = self.get_routines()
            await asyncio.gather(*tasks)
        except Exception as ex:
            await self._logger.error(str(ex))

    def get_routines(self):
        tasks = []
        tasks.append(self.run_mqtt_client())
        tasks.append(self.prepare_mqtt_publish_client())
        tasks.append(self._main_wrapper())
        tasks.append(self._idle_loop())
        return tasks

    async def run_mqtt_client(self):
        async with MQTTAsyncClient(id=self.id, host=self.host, port=self.port) as client:
            await client.connect()
            self.setup_process_message(client=client)
            await self._setup_command_handlers(client)
            await client.loop_forever()

    async def prepare_mqtt_publish_client(self):
        self._mqtt_client = MQTTAsyncClient(id=self.create_id(), host=self.host, port=self.port)
        await self._mqtt_client.connect()

    def get_handlers(self):
        return dict()

    def get_command_handlers(self):
        return self._command_handlers

    def setup_process_message(self, client):
        client.process_message = self._process_message

    def get_mqtt_client(self):
        return self._mqtt_client

    async def _main_wrapper(self):
        client = self.get_mqtt_client()
        if (self._main_callback):
            await self._main_callback(client)
        else:
            await self.on_main(client)

    async def on_main(self, client):
        pass

    async def _idle_loop(self):
        while True:
            try:
                if(self._on_idle):
                    await self._on_idle()
                else:
                    await self.on_idle()
            except Exception as ex:
                await self._logger.error(str(ex))
            finally:
                await asyncio.sleep(self.get_idle_delay())

    async def on_idle(self):
        pass

    def get_idle_delay(self):
        return self._idle_delay

    async def _setup_command_handlers(self, client):
        topics = set()
        if (not self._handlers):
            for k, v in self.get_handlers().items():
                self._command_handlers[k] = v
                topics.add(k)
        else:
            for k, v in self._handlers.items():
                self._command_handlers[k] = v
                topics.add(k)
        await client.subscribe(topics)

    async def _process_message(self, topic, payload):
        handler = self._command_handlers.get(topic, None)
        if (handler is not None):
            if inspect.iscoroutinefunction(handler):
                params = len(inspect.signature(handler).parameters)
                if (params == 2):
                    await handler(topic, payload)
                elif (params == 3):
                    await handler(topic, payload, self.get_mqtt_client())
            else:
                await asyncio.get_event_loop().run_in_executor(None, handler, topic, payload)
