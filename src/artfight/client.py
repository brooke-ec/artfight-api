from __future__ import annotations

from artfight.http import HTTPClient
from artfight.object import PartialUser, User

__all__ = ("ArtfightClient",)


class ArtfightClient:
    def __init__(self, username: str, password: str) -> None:
        self.http: HTTPClient = HTTPClient(username, password)

    async def __aenter__(self) -> ArtfightClient:
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the client's HTTP connection if it exists."""
        await self.http.close()

    def get_user(self, name: str) -> PartialUser:
        return PartialUser(name, self.http)

    async def fetch_user(self, name: str) -> User:
        return await self.get_user(name).fetch()
