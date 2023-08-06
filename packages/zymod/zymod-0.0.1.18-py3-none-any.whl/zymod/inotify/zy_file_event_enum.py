from enum import IntEnum, unique

import pyinotify


# noinspection PyUnresolvedReferences
@unique
class ZyFileEventEnum(IntEnum):
    IN_ACCESS = pyinotify.IN_ACCESS
    IN_MODIFY = pyinotify.IN_MODIFY
    IN_ATTRIB = pyinotify.IN_ATTRIB
    IN_CLOSE_WRITE = pyinotify.IN_CLOSE_WRITE
    IN_CLOSE_NOWRITE = pyinotify.IN_CLOSE_NOWRITE
    IN_OPEN = pyinotify.IN_OPEN
    IN_MOVED_FROM = pyinotify.IN_MOVED_FROM
    IN_MOVED_TO = pyinotify.IN_MOVED_TO
    IN_CREATE = pyinotify.IN_CREATE
    IN_DELETE = pyinotify.IN_DELETE
    IN_DELETE_SELF = pyinotify.IN_DELETE_SELF
    IN_MOVE_SELF = pyinotify.IN_MOVE_SELF
