from __future__ import annotations

from datetime import datetime
from typing import Any, List

from bs4 import BeautifulSoup, ResultSet, Tag

from artfight.http import HTTPClient
from artfight.object import user
from artfight.object.abc import ArtfightObject
from artfight.object.character import PartialCharacter
from artfight.parser import BaseParser
from artfight.util import (
    DATE_FORMAT,
    RE_BACKGROUND_IMAGE,
    RE_CHARACTER_URL,
    table_to_dict,
)

__all__ = ("PartialAttack", "Attack")


class AttackParser(BaseParser["Attack"]):
    _ROUTE = "/attack/%s"

    def parse(self, data: str, *args: Any) -> Attack:
        result = Attack(args[0], self.http)
        soup = BeautifulSoup(data, "html.parser")
        header = soup.select_one(".profile-header")

        # Extract Thumbnail
        icon = header.find("span", {"class": "icon-attack"})  # type: ignore
        result._thumbnail = RE_BACKGROUND_IMAGE.search(icon.attrs.get("style")).group(1)  # type: ignore

        # Extract Date Submitted
        card = soup.select_one(".profile-header-mobile-status > .card > .card-body")  # type: ignore
        submitted_date: ResultSet[Tag] = card.find_all("div", recursive=False)[1]  # type: ignore
        result._date_submitted = datetime.strptime(
            submitted_date.find(text=True, recursive=False),  # type: ignore
            DATE_FORMAT,
        )

        # Extract Image
        result._image = soup.select_one("#image-pane").find("img").attrs.get("src")  # type: ignore

        # Extract Info
        info_tag = soup.find("div", {"class": "card-header"}, string="Attack Info").parent.find("table")  # type: ignore
        info = table_to_dict(info_tag)  # type: ignore

        result._attacker = user.PartialUser(info["From"].find("a").text.strip(), self.http)  # type: ignore
        result._defender = user.PartialUser(info["To"].find("a").text.strip(), self.http)  # type: ignore
        result._team = info["Team"].find("a").text  # type: ignore

        # Extract Characters
        result._characters = []
        links: ResultSet[Tag] = info_tag.find_all("a")  # type: ignore
        for link in links:
            href = link.attrs.get("href")
            if href is None:
                continue
            match = RE_CHARACTER_URL.search(href)
            if match is None:
                continue
            char = PartialCharacter(int(match.group(1)), self.http)
            if char not in result._characters:
                result._characters.append(char)

        # Extract Stats
        stats_tag = soup.find("div", {"class": "card-header"}, string="Attack Stats").parent.find("table")  # type: ignore
        stats = table_to_dict(stats_tag)  # type: ignore

        result._points = int(stats["Points"].text)
        result._type = stats["Type"].text

        return result


class PartialAttack(ArtfightObject[int, "Attack"]):
    """Represents an Artfight attack that does not have all data present."""

    _PARSER = AttackParser
    _URL = "/attack/%s"


class Attack(PartialAttack):
    """Represents an Artfight attack."""

    def __init__(self, id: int, http: HTTPClient) -> None:
        super().__init__(id, http)
        self._characters: List[PartialCharacter]
        self._attacker: user.PartialUser
        self._defender: user.PartialUser
        self._date_submitted: datetime
        self._thumbnail: str
        self._points: int
        self._title: str
        self._type: str
        self._image: str
        self._team: str

    @property
    def characters(self) -> List[PartialCharacter]:
        """All the characters present in this attack."""
        return self._characters

    @property
    def attacker(self) -> user.PartialUser:
        """The user who submitted this attack."""
        return self._attacker

    @property
    def defender(self) -> user.PartialUser:
        """The user this attack was against."""
        return self._defender

    @property
    def date_submitted(self) -> datetime:
        """The datetime this attack was submitted."""
        return self._date_submitted

    @property
    def thumbnail(self) -> str:
        """The url to this attack's thumbnail."""
        return self._thumbnail

    @property
    def points(self) -> int:
        """The number of points this attack rewarded the attacker's team."""
        return self._points

    @property
    def title(self) -> str:
        """The title of the attack."""
        return self._title

    @property
    def type(self) -> str:
        """The type of media uploaded in the attack."""
        return self._type

    @property
    def image(self) -> str:
        """The url to this attack's main image."""
        return self._image

    @property
    def team(self) -> str:
        """The team of the attacker."""
        return self._team
