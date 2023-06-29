from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from artfight.http import Route

__all__ = (
    "ArtfightError",
    "HTTPError",
    "NotFoundError",
    "ArtfightServerError",
    "NotAuthenticated",
    "HTTPResponseError",
)


class ArtfightError(Exception):
    """Base exception for artfight-api modeule"""

    def __init__(self, *args: object) -> None:
        message = (type(self).__doc__,) if len(args) <= 0 else args
        super().__init__(*message)


class HTTPError(ArtfightError):
    """There was an error making the HTTP request"""


class NotAuthenticated(HTTPError):
    """The client tried to make an authenticated request but is not authenticated"""


class HTTPResponseError(HTTPError):
    """An error was caused by the request's response"""

    def __init__(self, route: "Route", status: Union[int, None] = None, *args: object) -> None:
        if status is not None and type(self) == HTTPError:
            super().__init__(f"{status} - Error making request")
        else:
            super().__init__()
        self.route = route


class UnauthorizedError(HTTPError):
    """Not authorized to access this resource"""


class NotFoundError(HTTPError):
    """Request returned 404"""


class ArtfightServerError(HTTPError):
    """The artfight servers may be experiencing difficulties"""
