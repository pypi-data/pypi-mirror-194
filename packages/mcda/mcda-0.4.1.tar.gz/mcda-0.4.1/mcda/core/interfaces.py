"""This module is used to gather core interfaces and encourage their use for
a more coherent API.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Trainer(Generic[T], ABC):
    """This interface describes a generic trainer."""

    @abstractmethod
    def train(self) -> T:  # pragma: nocover
        """Train and return an object.

        :return:
        """
        pass
