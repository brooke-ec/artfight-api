import re
from typing import Dict, Literal, Union

from bs4 import ResultSet, Tag

Method = Union[Literal["GET"], Literal["POST"], Literal["PUT"], Literal["DELETE"]]
RE_BACKGROUND_IMAGE = re.compile(r"background-image: url\((.+)\)")
RE_CHARACTER_URL = re.compile(r"\/character/(\d+)\..+")
DATE_FORMAT = "%d %B %Y %I:%M:%S %p"


def table_to_dict(root: Tag) -> Dict[str, Tag]:
    result: Dict[str, Tag] = {}
    rows: ResultSet[Tag] = root.find_all("tr", recursive=False)
    for row in rows:
        cells: ResultSet[Tag] = row.find_all("td", recursive=False)
        result[cells[0].text.strip(": ")] = cells[1]
    return result
