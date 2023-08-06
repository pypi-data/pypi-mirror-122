import logging

class SyncLoggerWrapper:
    def __init__(self, name) -> None:
        self._logger = logging.getLogger(name=name)
        self._name = name

    def get_name(self):
        return self._name

    def info(self, msg):
        self._logger.info(msg=msg)
    
    def warning(self, msg):
        self._logger.info(msg=msg)
    
    def debug(self, msg):
        self._logger.debug(msg=msg)

    def error(self, msg):
        self._logger.error(msg=msg)
