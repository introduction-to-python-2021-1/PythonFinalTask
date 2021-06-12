"""All constants used in the application."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

DATE_OR_SOURCE_IS_REQUIRED: Final[
    str
] = "At least one of the 'date' or 'source' arguments must be specified!\n"
DUMP_FILE: Final[str] = "ap-rss-reader-dump.json"
GREETING: Final[str] = (
    "The software is provided 'as is', without warranty of any kind,"
    " express or implied."
)
TITLE: Final[str] = "AP RSS-reader"
