from endpointlib.helpers.loggers.logger_manager import LoggerManager

class Device:
    def __init__(self, connection):
        self._connection = connection
        self._logger = LoggerManager.get_async_logger(name='endpointlib')

    async def send_command(self, command):
        try:
            await self._connection.connect()
            try:
                raw = await self._connection.send_string(command)
            finally:
                await self._connection.disconnect()
            return self.process_response(raw)
        except Exception as ex:
            await self._logger.error(str(ex))
        return self.no_response()

    # In case someone needs to process the response and return
    # something else then inherit this method
    def process_response(self, raw):
        return raw
    
    # If someone needs to return other str than None then inherit
    # this method
    def no_response(self):
        return ''

    def get_logger(self):
        return self._logger
