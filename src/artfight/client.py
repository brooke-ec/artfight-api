from __future__ import annotations

from artfight.http import HTTPClient
from artfight.object import Attack, PartialAttack, PartialUser, User

__all__ = ("ArtfightClient",)


class ArtfightClient:
    """Represents a connection to Artfight."""

    def __init__(self, username: str, password: str) -> None:
        """Represents a connection to Artfight.

        Parameters
        ----------
        username : str
            The username to log in with.
        password : str
            The password to log in with.
        """
        self.http: HTTPClient = HTTPClient(username, password)

    async def __aenter__(self) -> ArtfightClient:
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the client's HTTP connection if it exists."""
        await self.http.close()

    def get_user(self, name: str) -> PartialUser:
        """Returns a `PartialUser` instance from their username.

        Parameters
        ----------
        name : str
            The username of the user to get.

        Returns
        -------
        PartialUser
            A `PartialUser` instance representing the user.
        """
        return PartialUser(name, self.http)

    async def fetch_user(self, name: str) -> User:
        """Fetches an up-to-date instance of a user.

        Parameters
        ----------
        name : str
            The username of the user to fetch.

        Returns
        -------
        User
            An instance of `User` representing the fetched user.
        """
        return await self.get_user(name).fetch()

    def get_attack(self, id: int) -> PartialAttack:
        """Returns a `PartialAttack` instance from its id.

        Parameters
        ----------
        id : int
            The attack id to get.

        Returns
        -------
        PartialAttack
           A `PartialAttack` instance representing the attack.
        """
        return PartialAttack(id, self.http)

    async def fetch_attack(self, id: int) -> Attack:
        """Fetches an up-to-date instance of an Attack.

        Parameters
        ----------
        id : int
            The id of the attack to fetch.

        Returns
        -------
        Attack
            An instance of `Attack` representing the fetched attack.
        """
        return await self.get_attack(id).fetch()
