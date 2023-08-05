from endpointlib.helpers.loggers.logger_stream import LoggerStream
from endpointlib.helpers.loggers.logger_level import LoggerLevel

class LoggerSettings:
    def __init__(self, stream, level, format) -> None:
        self._stream = stream
        self._level = level
        self._format = format
    
    def get_stream(self):
        return self._stream
    
    def get_level(self):
        return self._level
    
    def get_format(self):
        return self._format

    # Static section
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @staticmethod
    def get_settings(stream, level, format=DEFAULT_FORMAT):
        return LoggerSettings(stream=stream, level=level, format=format)

    @staticmethod
    def get_default_settings():
        return LoggerSettings(stream=LoggerStream.stdout,
                    level=LoggerLevel.CRITICAL, format=LoggerSettings.DEFAULT_FORMAT)

    @staticmethod
    def get_debug_settings(level=LoggerLevel.DEBUG):
        return LoggerSettings(stream=LoggerStream.stdout,
                    level=level, format=LoggerSettings.DEFAULT_FORMAT)
