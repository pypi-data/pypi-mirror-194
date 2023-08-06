from enum import unique, IntEnum


@unique
class ZyEventLevel(IntEnum):
    Notice = 0
    Warning = 1
    Alert = 2
