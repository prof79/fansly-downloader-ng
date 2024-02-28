"""Download Types"""

from strenum import StrEnum
from enum import auto


class DownloadType(StrEnum):
    NOTSET = auto()
    COLLECTIONS = auto()
    MESSAGES = auto()
    SINGLE = auto()
    TIMELINE = auto()
