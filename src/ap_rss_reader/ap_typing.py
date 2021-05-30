"""All types used in the application."""

from __future__ import annotations

from typing import List
from typing import Literal
from typing import TypedDict

HelloWorld = Literal["Hello, World!"]


class ItemAsDict(TypedDict):
    """Implementation of an item in the form of a dictionary."""

    title: str
    link: str
    date: str
    source: str
    source_url: str
    media_content_url: str


class ChannelAsDict(TypedDict):
    """Implementation of a channel in the form of a dictionary."""

    title: str
    items: List[ItemAsDict]
