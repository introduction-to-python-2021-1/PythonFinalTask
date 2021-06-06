"""All types used in the application."""

from __future__ import annotations

from typing import Callable
from typing import Literal

from ap_rss_reader.ap_collections import ChannelItem

Filter = Callable[[ChannelItem], bool]
HelloWorld = Literal["Hello, World!"]
