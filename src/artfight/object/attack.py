from __future__ import annotations

from typing import Any

from artfight.http import HTTPClient
from artfight.object.abc import ArtfightObject
from artfight.parser import BaseParser

__all__ = ("PartialAttack", "Attack")


class AttackParser(BaseParser["Attack"]):
    _ROUTE = "/attack/%s"

    def parse(self, data: str, *args: Any) -> Attack:
        result = Attack(args[0], self.http)

        return result


class PartialAttack(ArtfightObject[int, "Attack"]):
    _PARSER = AttackParser


class Attack(PartialAttack):
    def __init__(self, id: int, http: HTTPClient) -> None:
        super().__init__(id, http)
