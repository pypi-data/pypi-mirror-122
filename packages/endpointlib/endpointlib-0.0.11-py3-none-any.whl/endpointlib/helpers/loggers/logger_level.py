from enum import Enum

class LoggerLevel(Enum):
    CRITICAL = 60
    FATAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0
