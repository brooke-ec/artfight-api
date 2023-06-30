from __future__ import annotations

from abc import ABC
from typing import Generic, Type, TypeVar

from artfight.http import HTTPClient
from artfight.parser import BaseParser

F = TypeVar("F", bound="ArtfightObject")
T = TypeVar("T")


class ArtfightObject(ABC, Generic[T, F]):
    _PARSER: Type[BaseParser[F]]

    def __init__(self, id: T, http: HTTPClient) -> None:
        self._http: HTTPClient = http
        self._id: T = id

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, type(self)) and self.id == __value.id

    @property
    def id(self) -> T:
        """The unique identifier for this object."""
        return self._id

    async def fetch(self) -> F:
        """Fetch a full instance of this partial."""
        parser = self._PARSER(self._http)
        return await parser.run(self.id)
