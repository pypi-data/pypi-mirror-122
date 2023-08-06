from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.levels import LogLevel

from endpointlib.helpers.loggers.logger_level import LoggerLevel

class AsyncLoggerWrapper:
    def __init__(self, name, settings) -> None:
        levelSw = {
            LoggerLevel.CRITICAL: LogLevel.CRITICAL,
            LoggerLevel.FATAL: LogLevel.FATAL,
            LoggerLevel.ERROR: LogLevel.ERROR,
            LoggerLevel.WARNING: LogLevel.WARNING,
            LoggerLevel.INFO: LogLevel.INFO,
            LoggerLevel.DEBUG: LogLevel.DEBUG,
            LoggerLevel.NOTSET: LogLevel.NOTSET,
        }
        level = levelSw.get(settings.get_level(), LogLevel.CRITICAL)

        self._logger = Logger.with_default_handlers(name=name,
                level=level, formatter=Formatter(settings.get_format()))
        self._name = name

    def get_name(self):
        return self._name

    async def info(self, msg):
        await self._logger.info(msg=msg)
    
    async def warning(self, msg):
        await self._logger.info(msg=msg)
    
    async def debug(self, msg):
        await self._logger.debug(msg=msg)

    async def error(self, msg):
        await self._logger.error(msg=msg)

    async def shutdown(self):
        await self._logger.shutdown()
