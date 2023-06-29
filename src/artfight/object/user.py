from __future__ import annotations

from datetime import datetime

from bs4 import BeautifulSoup, ResultSet, Tag

from artfight.http import HTTPClient, Route
from artfight.object.abc import ArtfightObject
from artfight.util import DATE_FORMAT

__all__ = ("PartialUser", "User")


class PartialUser(ArtfightObject[str]):
    @property
    def name(self) -> str:
        return self.id

    async def fetch(self) -> User:
        data = await self.http.request(Route("GET", "/~%s", self.name))
        i = User(self.name, self.http)
        soup = BeautifulSoup(data, features="html.parser")

        # fmt: off
        card = soup.select_one(".profile-header > .profile-header-mobile-status > .card > .card-body")
        info: ResultSet[Tag] = card.find_all("p", {"class": "text-right"})  # type: ignore
        i._date_joined = datetime.strptime(info[0].find("span").attrs.get("title"), DATE_FORMAT)  # type: ignore
        i._last_seen = datetime.strptime(info[1].text, DATE_FORMAT)
        i._team = info[2].text
        # fmt: on

        return i


class User(PartialUser):
    def __init__(self, id: str, http: HTTPClient) -> None:
        super().__init__(id, http)

        self._date_joined: datetime
        self._last_seen: datetime
        self._team: str

    @property
    def date_joined(self) -> datetime:
        return self._date_joined

    @property
    def last_seen(self) -> datetime:
        return self._last_seen

    @property
    def team(self) -> str:
        return self._team
