from __future__ import annotations

from datetime import datetime
from typing import Any, AsyncIterator, Dict, List, Tuple

from bs4 import BeautifulSoup, ResultSet, Tag

from artfight.http import HTTPClient
from artfight.object import attack
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
        result._avatar = RE_BACKGROUND_IMAGE.search(icon.attrs.get("style")).group(1)  # type: ignore

        card = header.select_one(".profile-header-mobile-status > .card > .card-body")  # type: ignore
        info: ResultSet[Tag] = card.find_all("p", {"class": "text-right"}, recursive=False)  # type: ignore

        # Extract Last Seen
        result._last_seen = None
        last_seen = info[0].span
        if last_seen is not None:
            result._last_seen = datetime.strptime(last_seen.attrs.get("title"), DATE_FORMAT)  # type: ignore

        # Extract Satus Info
        result._date_joined = datetime.strptime(info[1].text, DATE_FORMAT)
        result._team = info[2].text

        # Extract Links
        result._links = {}
        links: ResultSet[Tag] = soup.select_one(".profile-links").find_all("tr", recursive=False)  # type: ignore
        for link in links:
            cells: ResultSet[Tag] = link.find_all("td", recursive=False)
            site = cells[0].strong.text  # type: ignore
            url = cells[1].a.attrs["href"]  # type: ignore
            result._links[site] = url

        return result


class AttackListParser(BaseParser[Tuple[List[attack.PartialAttack], bool]]):
    _ROUTE = "/~%s/attacks?page=%s"

    def parse(self, data: str, *args: Any) -> Tuple[List[attack.PartialAttack], bool]:
        result: List[attack.PartialAttack] = []
        soup = BeautifulSoup(data, features="html.parser")

        # Extract List
        body: Tag = soup.select_one(".profile-attacks-body")  # type: ignore
        list = body.find("div", {"class": "row clearfix"})
        attacks: ResultSet[Tag] = list.find_all("div", recursive=False)  # type: ignore
        for a in attacks:
            id = int(a.a.attrs.get("data-id"))  # type: ignore
            result.append(attack.PartialAttack(id, self.http))

        # Extract EOF
        eof = True
        nav = body.select_one("nav")
        if nav is not None:
            eof = nav.select("ul.pagination > li")[-1].attrs.get("aria-disabled") == "true"  # type: ignore

        return result, eof


class PartialUser(ArtfightObject[str, "User"]):
    _PARSER = ProfileParser

    def __init__(self, id: str, http: HTTPClient) -> None:
        super().__init__(id, http)

    @property
    def name(self) -> str:
        """The username of this artfight user."""
        return self.id

    async def fetch_attacks(self) -> AsyncIterator[attack.PartialAttack]:
        """Asynchronously fetches all the attacks this user has made.

        Returns
        -------
        AsyncIterator[attack.PartialAttack]
            The `PartialAttacks` representing this user's attacks.
        """
        parser = AttackListParser(self._http)
        eof = False
        count = 1
        while not eof:
            page, eof = await parser.run(self.name, count)
            for i in page:
                yield i
            count += 1


class User(PartialUser):
    def __init__(self, id: str, http: HTTPClient) -> None:
        super().__init__(id, http)
        self._last_seen: datetime | None
        self._links: Dict[str, str]
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
