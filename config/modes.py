"""Download Modes"""

from strenum import StrEnum
from enum import auto


class DownloadMode(StrEnum):
    NOTSET = auto()
    COLLECTION = auto()
    MESSAGES = auto()
    NORMAL = auto()
    POSTS = auto()
    TIMELINE = auto()
