"""All types used in the application."""

from __future__ import annotations

from typing import Callable

from ap_rss_reader.ap_collections import Article

Filter = Callable[[Article], bool]
