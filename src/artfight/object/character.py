from __future__ import annotations

from typing import Optional

from artfight.http import HTTPClient
from artfight.object.abc import ArtfightObject


class PartialCharacter(ArtfightObject[int, "Character"]):
    """Represents an Artfight character that does not have all data present."""

    def __init__(self, id: int, http: HTTPClient) -> None:
        super().__init__(id, http)
        self._name: str

    @property
    def name(self) -> Optional[str]:
        """The name of this character."""
        return self._get_attr("_name")


class Character(PartialCharacter):
    """Represents an Artfight character."""

    @property
    def name(self) -> str:
        """The name of this character."""
        return self._name
