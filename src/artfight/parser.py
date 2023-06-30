from __future__ import annotations

import logging
import traceback
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from artfight import __repo__, error
from artfight.http import HTTPClient
from artfight.util import Method

_log = logging.getLogger(__name__)

T = TypeVar("T")

__all__ = ("BaseParser",)


class BaseParser(ABC, Generic[T]):
    _METHOD: Method = "GET"
    _ROUTE: str

    def __init__(self, http: HTTPClient) -> None:
        self.http: HTTPClient = http

    async def run(self, *args: Any) -> T:
        """Run the parser and returned the result.

        Wrapper around `fetch` and `parse`

        Parameters
        ----------
        args : tuple[Any]
            Arbitrary arguments to supply to the parser.

        Returns
        -------
        T
            The resultant object.

        Raises
        ------
        error.ParseError
            Raised when there is an error parsing the markdown, ensure you are using the latest version.
        """
        data: str = await self.fetch(*args)

        try:
            return self.parse(data, *args)
        except (AttributeError, IndexError) as e:
            msg = f"Error Parsing using {type(self)} : {args}"
            _log.error(
                "%s - Please report this error to %s/issues/new\n%s",
                msg,
                __repo__,
                traceback.format_exc(),
            )
            raise error.ParseError(msg) from e

    async def fetch(self, *args: Any) -> str:
        """Fetches the markdown for the parser.

        Parameters
        ----------
        args : tuple[Any]
            The arguments supplied when calling the parser.

        Returns
        -------
        str
            The fetched markdown.
        """
        return await self.http.request(self._METHOD, self._ROUTE % args)

    @abstractmethod
    def parse(self, data: str, *args: Any) -> T:
        """Parses the markdown recieved from the fetch method.

        Parameters
        ----------
        data : str
            The markdown recieved.
        args : tuple[Any]
            The arguments supplied when calling the parser.

        Returns
        -------
        T
            The resultant object.
        """
