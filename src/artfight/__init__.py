"""A module for retrieving data from [artfight](https://artfight.net/)."""

__all__ = (
    "ArtfightClient",
    "Attack",
    "PartialAttack",
    "PartialUser",
    "User",
    "ArtfightError",
    "HTTPError",
    "LoginError",
    "ParseError",
)
__repo__ = r"https://github.com/NimajnebEC/artfight-api"
__version__ = "0.1.2"

from artfight.client import ArtfightClient
from artfight.error import ArtfightError, HTTPError, LoginError, ParseError
from artfight.object import Attack, PartialAttack, PartialUser, User
