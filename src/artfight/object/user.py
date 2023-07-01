from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from bs4 import BeautifulSoup, ResultSet, Tag

from artfight.http import HTTPClient
from artfight.object.abc import ArtfightObject
from artfight.parser import BaseParser
from artfight.util import DATE_FORMAT, RE_BACKGROUND_IMAGE

__all__ = ("PartialUser", "User")


class ProfileParser(BaseParser["User"]):
    _ROUTE = "/~%s"

    def parse(self, data: str, *args: Any) -> User:
        result = User(args[0], self.http)
        soup = BeautifulSoup(data, features="html.parser")
        header = soup.select_one(".profile-header")

        # Extract Avatar
        icon = soup.find("span", {"class": "icon-user"})
        result._avatar = RE_BACKGROUND_IMAGE.search(icon.attrs["style"]).group(1)  # type: ignore

        card = header.select_one(".profile-header-mobile-status > .card > .card-body")  # type: ignore
        info: ResultSet[Tag] = card.find_all("p", {"class": "text-right"})  # type: ignore

        # Extract Last Seen
        result._last_seen = None
        last_seen = info[0].find("span")
        if last_seen is not None:
            result._last_seen = datetime.strptime(last_seen.attrs.get("title"), DATE_FORMAT)  # type: ignore

        # Extract Satus Info
        result._date_joined = datetime.strptime(info[1].text, DATE_FORMAT)
        result._team = info[2].text

        # Extract Links
        result._links = {}
        links = soup.select_one(".profile-links").find_all("tr")  # type: ignore
        for link in links:
            cells: ResultSet[Tag] = link.find_all("td")
            site = cells[0].find("strong").text  # type: ignore
            url = cells[1].find("a").attrs["href"]  # type: ignore
            result._links[site] = url

        return result


class PartialUser(ArtfightObject[str, "User"]):
    _PARSER = ProfileParser

    @property
    def name(self) -> str:
        return self.id


class User(PartialUser):
    def __init__(self, id: str, http: HTTPClient) -> None:
        super().__init__(id, http)
        self._links: Dict[str, str]
        self._last_seen: datetime | None
        self._date_joined: datetime
        self._avatar: str
        self._team: str

    @property
    def avatar(self) -> str:
        """The URL of this user's avatar."""
        return self._avatar

    @property
    def date_joined(self) -> datetime:
        """The datetime of when this user joined artfight."""
        return self._date_joined

    @property
    def last_seen(self) -> datetime | None:
        """The datetime of when this user was last seen online, `None` if hidden."""
        return self._last_seen

    @property
    def team(self) -> str:
        """The team this user is part of."""
        return self._team

    @property
    def links(self) -> Dict[str, str]:
        """Dictionary containing this user's social links."""
        return self._links
