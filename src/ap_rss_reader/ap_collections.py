"""All collections used in the application."""

from __future__ import annotations

from datetime import datetime
from typing import NamedTuple
from typing import Optional


class Article(NamedTuple):
    """The smallest chunk (news) of rss channel."""

    title: str
    link: str
    date: datetime
    source: str
    source_url: str
    media_content_url: str


class Media(NamedTuple):
    """The media content of rss article."""

    type: str
    url: str
    height: Optional[str]
    width: Optional[str]
