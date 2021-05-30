"""All collections used in the application."""

from __future__ import annotations

from datetime import datetime
from typing import NamedTuple


class ChannelItem(NamedTuple):
    """The smallest chunk (news) of rss channel."""

    title: str
    link: str
    date: datetime
    source: str
    source_url: str
    media_content_url: str


class Channel(NamedTuple):
    """RSS Feed."""

    title: str
    items: list[ChannelItem]
