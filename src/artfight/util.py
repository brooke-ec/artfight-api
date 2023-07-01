import re
from typing import Literal, Union

Method = Union[Literal["GET"], Literal["POST"], Literal["PUT"], Literal["DELETE"]]
RE_BACKGROUND_IMAGE = re.compile(r"background-image: url\((.+)\)")
DATE_FORMAT = "%d %B %Y %I:%M:%S %p"
