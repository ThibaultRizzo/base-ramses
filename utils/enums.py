"""
Module for generic enum utilities
"""
from enum import Enum


class BaseEnum(str, Enum):
    """
    Base enum to handle stringification of value
    """

    def __str__(self):
        return self.value
