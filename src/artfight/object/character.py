from __future__ import annotations

from artfight.object.abc import ArtfightObject


class PartialCharacter(ArtfightObject[int, "Character"]):
    ...


class Character(PartialCharacter):
    ...
