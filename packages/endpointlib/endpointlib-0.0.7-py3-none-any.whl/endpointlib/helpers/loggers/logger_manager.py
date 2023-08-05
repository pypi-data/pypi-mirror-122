import logging
import sys

from endpointlib.helpers.loggers.async_logger_wrapper import AsyncLoggerWrapper
from endpointlib.helpers.loggers.logger_settings import LoggerSettings
from endpointlib.helpers.loggers.logger_stream import LoggerStream
from endpointlib.helpers.loggers.logger_level import LoggerLevel
from endpointlib.helpers.loggers.sync_logger_wrapper import SyncLoggerWrapper

class LoggerManager:
    def __init__(self) -> None:
        self._sync_loggers = dict()
        self._async_loggers = dict()
        self._settings = None

    def _get_async_logger(self, name):
        if (name not in self._async_loggers):
            self._async_loggers[name] = AsyncLoggerWrapper(name, self._settings)
        return self._async_loggers[name]

    def _get_sync_logger(self, name):
        if (name not in self._sync_loggers):
            self._sync_loggers[name] = SyncLoggerWrapper(name)
        return self._sync_loggers[name]

    def _has_settings(self):
        return self._settings is not None

    def _setup(self, settings):
        # setup sync logging
        streamSw = {
            LoggerStream.stdout: sys.stdout,
            LoggerStream.stdin: sys.stdin,
            LoggerStream.stderr: sys.stderr,
        }
        stream = streamSw.get(settings.get_stream(), sys.stdout)

        levelSw = {
            LoggerLevel.CRITICAL: logging.CRITICAL,
            LoggerLevel.FATAL: logging.FATAL,
            LoggerLevel.ERROR: logging.ERROR,
            LoggerLevel.WARNING: logging.WARNING,
            LoggerLevel.INFO: logging.INFO,
            LoggerLevel.DEBUG: logging.DEBUG,
            LoggerLevel.NOTSET: logging.NOTSET,
        }
        level = levelSw.get(settings.get_level(), logging.CRITICAL)

        logging.basicConfig(stream=stream, level=level, format=settings.get_format())

        # store settings for async loggers
        self._settings = settings

    # Static section
    _INSTANCE = None

    @staticmethod
    def create(settings):
        if (not LoggerManager._INSTANCE):
            LoggerManager._INSTANCE = LoggerManager()
        LoggerManager._INSTANCE._setup(settings=settings)

    @staticmethod
    def _get_instance():
        if (not LoggerManager._INSTANCE):
            # If no settings then create with default settings
            LoggerManager.create(LoggerSettings.get_default_settings())
        return LoggerManager._INSTANCE

    @staticmethod
    def get_sync_logger(name):
        manager = LoggerManager._get_instance()
        return manager._get_sync_logger(name=name)

    @staticmethod
    def get_async_logger(name):
        manager = LoggerManager._get_instance()
        return manager._get_async_logger(name=name)