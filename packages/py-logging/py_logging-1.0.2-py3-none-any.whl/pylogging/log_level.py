import enum


class LogLevel(enum.Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3


class LogLevelError(Exception):
    pass
