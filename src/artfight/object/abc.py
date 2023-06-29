from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from artfight.http import HTTPClient

T = TypeVar("T")


class ArtfightObject(ABC, Generic[T]):
    def __init__(self, id: T, http: HTTPClient) -> None:
        self.http: HTTPClient = http
        self._id: T = id

    @property
    def id(self) -> T:
        """The unique identifier for this object."""
        return self._id

    @abstractmethod
    async def fetch(self) -> ArtfightObject[T]:
        """Fetch a full instance of this partial."""
