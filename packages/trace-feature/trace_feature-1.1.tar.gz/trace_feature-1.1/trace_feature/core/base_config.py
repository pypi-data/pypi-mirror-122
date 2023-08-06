"""
    Base config for ABC method
"""

from abc import ABC, abstractmethod


class BaseConfig(ABC):
    """
        BaseConfig class
    """

    @abstractmethod
    def config(self):
        """
            BaseConfig config self
        """
