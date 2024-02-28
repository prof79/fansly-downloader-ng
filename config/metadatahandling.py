"""Metadata Handling"""

from strenum import StrEnum
from enum import auto


class MetadataHandling(StrEnum):
    NOTSET = auto()
    ADVANCED = auto()
    SIMPLE = auto()
