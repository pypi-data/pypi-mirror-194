from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


@dataclass
class PlexServerConfig:
    """
    Class to hold single server config
    """

    name: str
    token: str
    urls: List[str]

    def asdict(self):
        data = asdict(self)
        del data["name"]

        return data
