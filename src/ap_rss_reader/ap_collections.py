"""All collections used in the application."""

from __future__ import annotations

from typing import NamedTuple
from typing import Optional


class Media(NamedTuple):
    """The media content of rss article."""

    type: str
    url: str
    height: Optional[str]
    width: Optional[str]
