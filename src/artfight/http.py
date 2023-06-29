from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any, Dict, Literal, Optional, Union
from urllib import parse as urlparse

import aiohttp

from artfight import __version__, error

_log = logging.getLogger(__name__)

Method = Union[Literal["GET"], Literal["POST"], Literal["PUT"], Literal["DELETE"]]

_RETRY_ATTEMPTS = 5
_SESSION_COOKIE = "laravel_session"


class Route:
    """Represents an Artfight route"""

    BASE: str = "https://artfight.net/"

    def __init__(self, method: Method, path: str, *args: str) -> None:
        self.url = urlparse.urljoin(self.BASE, path % args)
        self.method = method


class HTTPClient:
    """HTTPClient handles all the HTTP requests performed by artfight-api"""

    def __init__(self) -> None:
        user_agent = "Artfight Bot (https://github.com/NimajnebEC/artfight-api v{0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
        self._client: Union[aiohttp.ClientSession, None] = None
        self._session: Union[str, None] = None

    async def __aenter__(self) -> HTTPClient:
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def close(self):
        """Closes the HTTP connection if it exists."""
        if self._client is not None:
            await self._client.close()

    async def request(
        self,
        route: Route,
        *,
        form: Optional[Dict[str, Any]] = None,
        authenticated: bool = True,
    ) -> str:
        """Wraps aiohttp requests

        Parameters
        ----------
        route : Route
            The route data to perform the request against
        form : Dict[str, Any], optional
            If specified, the form data to include in the body of the request., by default None.
        authenticated : bool, optional
            Wether the client should be authenticated to perform this request, by default True.

        Returns
        -------
        str
            The HTML returned by the request.

        Raises
        ------
        NotAuthenticated
            Raised when an authenticated request is attempted before the client has logged in.
        UnauthorizedError
            Raised when trying to access a protected route when not logged in.
        NotFoundError
            Raised when the server replies with 404.
        ArtfightServerError
            Raised when an error occurs on the artfight servers.
        HTTPResponseError
            Raised when an arbitrary response it recieved.
        RuntimeError
            Raised when the HTTP connection has not been initialised.
        """
        method = route.method
        url = route.url
        data = None

        # ensure Client is setup
        if self._client is None:
            raise RuntimeError("HTTP connection not open")

        # initialise headers
        headers: dict[str, str] = {
            "User-Agent": self.user_agent,
        }

        # add session cookie if exists
        if self._session is None:
            if authenticated:
                raise error.NotAuthenticated()
        else:
            headers["Cookie"] = f"{_SESSION_COOKIE}={self._session}"

        # add form data if applicable
        if form is not None:
            data = aiohttp.FormData(form)

        response = None
        for tries in range(_RETRY_ATTEMPTS):
            await asyncio.sleep(tries * 2)

            try:
                async with self._client.request(
                    allow_redirects=False,
                    method=route.method,
                    headers=headers,
                    url=route.url,
                    data=data,
                ) as response:
                    _log.debug("%s %s : %s", method, url, response.status)

                    # update session
                    token = response.cookies.get(_SESSION_COOKIE)
                    if token is not None:
                        self._session = token.value

                    # successful request
                    if 300 > response.status >= 200:
                        return await response.text()

                    # redirected
                    if response.status == 302:
                        # check redirected to login (unauthorized)
                        location = response.headers.get("Location")
                        if location == Route("GET", "/login").url:
                            raise error.UnauthorizedError(route)
                        return ""

                    # unconditional retry
                    if response.status in (500, 502, 504, 524):
                        continue

                    # special errors
                    elif response.status == 404:
                        raise error.NotFoundError(route)
                    elif response.status >= 500:
                        raise error.ArtfightServerError(route)
                    else:
                        raise error.HTTPResponseError(route, response.status)

            except OSError as e:
                # connection reset
                if e.errno in (54, 10054):
                    continue
                raise

        if response is not None:
            # We've run out of retries, raise.
            if response.status >= 500:
                raise error.ArtfightServerError(route)
            raise error.HTTPResponseError(route, response.status)

        raise RuntimeError("_RETRY_ATTEMPTS was < 1")

    async def login(self, username: str, password: str) -> None:
        """Login to the artfight servers using the specified credentials

        Parameters
        ----------
        username : str
            The username to log in with
        password : str
            The password to log in with

        Raises
        ------
        ValueError
            Raised when the specified credentials are invalid
        """
        if self._client is None:
            self._client = aiohttp.ClientSession()

        try:
            await self.request(
                Route("POST", "/login"),
                authenticated=False,
                form={"username": username, "password": password},
            )
        except error.UnauthorizedError:
            raise ValueError("Invalid login credentials")
