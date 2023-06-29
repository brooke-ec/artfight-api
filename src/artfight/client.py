from __future__ import annotations

from artfight.http import HTTPClient
from artfight.object import PartialUser, User

__all__ = ("ArtfightClient",)


class ArtfightClient:
    def __init__(self) -> None:
        self.http: HTTPClient = HTTPClient()

    async def __aenter__(self) -> ArtfightClient:
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the client's HTTP connection if it exists."""
        await self.http.close()

    async def login(self, username: str, password: str) -> None:
        """Login to the artfight servers using the specified credentials

        Parameters
        ----------
        username : str
            The username to log in with
        password : str
            The password to log in with

        Raises
        ------
        ValueError
            Raised when the specified credentials are invalid
        """
        await self.http.login(username, password)

    def get_user(self, name: str) -> PartialUser:
        return PartialUser(name, self.http)

    async def fetch_user(self, name: str) -> User:
        return await self.get_user(name).fetch()
