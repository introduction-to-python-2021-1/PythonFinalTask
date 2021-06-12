"""All collections used in the application."""

from __future__ import annotations

from datetime import datetime
from typing import NamedTuple


class Article(NamedTuple):
    """The smallest chunk (news) of rss channel."""

    title: str
    link: str
    date: datetime
    source: str
    source_url: str
    media_content_url: str
