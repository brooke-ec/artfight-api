from typing import Union

from artfight.util import Method

__all__ = (
    "ArtfightError",
    "HTTPError",
    "NotFoundError",
    "ArtfightServerError",
    "HTTPResponseError",
)


class ArtfightError(Exception):
    """Base exception for artfight-api modeule"""

    def __init__(self, *args: object) -> None:
        message = (type(self).__doc__,) if len(args) <= 0 else args
        super().__init__(*message)


class LoginError(ArtfightError):
    """The provided login credentials were not accepted by the server"""


class ParseError(ArtfightError):
    """There was an error parsing markdown"""


class HTTPError(ArtfightError):
    """There was an error making the HTTP request"""


class HTTPResponseError(HTTPError):
    """An error was caused by the request's response"""

    def __init__(
        self,
        method: Method,
        url: str,
        status: Union[int, None] = None,
        *args: object,
    ) -> None:
        if status is not None:
            super().__init__(f"{method} {url} - Error {status}")
        else:
            super().__init__(*args)
        self.method: Method = method
        self.url: str = url


class UnauthorizedError(HTTPError):
    """Not authorized to access this resource"""


class NotFoundError(HTTPError):
    """Request returned 404"""


class ArtfightServerError(HTTPError):
    """The artfight servers may be experiencing difficulties"""
