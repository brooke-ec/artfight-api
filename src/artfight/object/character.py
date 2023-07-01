from __future__ import annotations

from artfight.object.abc import ArtfightObject


class PartialCharacter(ArtfightObject[int, "Character"]):
    """Represents an Artfight character that does not have all data present."""


class Character(PartialCharacter):
    """Represents an Artfight character."""
