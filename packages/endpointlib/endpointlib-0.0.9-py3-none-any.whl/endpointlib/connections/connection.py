from endpointlib.helpers.loggers.logger_manager import LoggerManager

class Connection:
    def __init__(self):
        self._logger = LoggerManager.get_async_logger(name='endpointlib')

    def is_connected(self):
        return False

    def get_logger(self):
        return self._logger

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def send(self, buffer):
        raise NotImplementedError
  
    async def send_string(self, data):
        response = await self.send(data.encode('utf-8'))
        if response:
           return response.decode('utf-8')
        return ''
