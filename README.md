# Artfight Api

A module for retrieving data from [artfight.net](https://artfight.net/).

Powered by [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) Artfight Api scrapes the normal frontend to retrieve data from Artfight. As a result any changes to the UI are likely to break this module. If you encounter any errors please be sure to report them to the repository's [GitHub issues page](https://github.com/NimajnebEC/artfight-api/issues/new).

## Quickstart

Install the module:

```
pip install artfight-api
```

Fetch all attacks by a user:

```py
import asyncio

from artfight import ArtfightClient


async def main():
    async with ArtfightClient("USERNAME", "PASSWORD") as client:
        async for attack in client.get_user("Takaia").fetch_attacks():
            fetched = await attack.fetch()
            print(fetched.title)


asyncio.run(main())
```
