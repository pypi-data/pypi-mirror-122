from endpointlib.connections.serial_connection import SerialConnection
from endpointlib.devices.device import Device

class SerialDevice(Device):
    def __init__(self, port, baudrate):
        super().__init__(SerialConnection(port=port, baudrate=baudrate))