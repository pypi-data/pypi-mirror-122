import asyncio

from endpointlib.connections.connection import Connection

class SocketConnection(Connection):
    def __init__(self, host, port):
        super().__init__()
        self._host = host
        self._port = port
        self._reader = None
        self._writer = None
    
    def is_connected(self):
        if (self._reader is not None and self._writer is not None):
            if (not self._writer.is_closing()):
                return True
        return False

    async def connect(self):
        try:           
            self._reader, self._writer = await asyncio.wait_for(asyncio.open_connection(
                    self._host, self._port) , 2)
        except Exception as ex:
            await self.get_logger().error(str(ex))
    
    async def send(self, buffer):
        response = None
        if (self.is_connected()):
            try:
                self._writer.write(buffer)
                await self._writer.drain()
                response = await asyncio.wait_for(self._reader.read(2048), 2)
            except Exception as ex:
                await self.get_logger().error(str(ex))
        return response

    async def disconnect(self):
        if (self.is_connected()):
            self._writer.close()
            await self._writer.wait_closed()
        self._reader = None
        self._writer = None
