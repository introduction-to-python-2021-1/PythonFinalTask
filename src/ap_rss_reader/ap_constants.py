"""All constants used in the application."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

DATE_OR_SOURCE_IS_REQUIRED: Final[
    str
] = "At least one of the 'date' or 'source' arguments must be specified!\n"
DUMP_FILE: Final[str] = "ap-rss-reader-dump.json"
ERROR_JSON_LOAD = "ERROR: File cannot be read: decoding JSON has failed."
ERROR_NO_DATA = "Sorry! There's no data that can be parsed."
GREETING: Final[str] = (
    "The software is provided 'as is', without warranty of any kind,"
    " express or implied."
)
APP_TITLE: Final[str] = "AP RSS-reader"
