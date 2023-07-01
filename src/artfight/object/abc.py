from __future__ import annotations

from abc import ABC
from typing import Any, Generic, Optional, Type, TypeVar

from artfight.http import BASE_URL, HTTPClient, join_url
from artfight.parser import BaseParser

F = TypeVar("F", bound="ArtfightObject")
T = TypeVar("T")


class ArtfightObject(ABC, Generic[T, F]):
    """Represents a structure from the artfight website."""

    _PARSER: Type[BaseParser[F]]
    _URL: str

    def __init__(self, id: T, http: HTTPClient) -> None:
        """Represents a structure from the artfight website.

        Parameters
        ----------
        id : T
            The unique identifier used to represent this object.
        http : HTTPClient
            An `HTTPClient` instance.
        """
        self._http: HTTPClient = http
        self._id: T = id

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, type(self)) and self.id == __value.id

    def __repr__(self) -> str:
        return f"<{type(self).__name__} id={repr(self.id)}>"

    def _get_attr(self, name: str) -> Optional[Any]:
        """Returns the specified attribute if it exists.

        Parameters
        ----------
        name : str
            The name of the attribute to get.

        Returns
        -------
        Optional[Any]
            The attribute, or `None` if it doesn't exist.
        """
        if hasattr(self, name):
            return getattr(self, name)
        return None

    @property
    def id(self) -> T:
        """The unique identifier for this object."""
        return self._id

    @property
    def url(self) -> str:
        """The url to this object."""
        if not hasattr(self, "_URL"):
            raise NotImplementedError("Object did not specify a url template.")
        return join_url(BASE_URL, self._URL % (self.id,))

    async def fetch(self) -> F:
        """Fetch a full instance of this partial."""
        if not hasattr(self, "_PARSER"):
            raise NotImplementedError("Object did not specify a parser.")
        parser = self._PARSER(self._http)
        return await parser.run(self.id)
