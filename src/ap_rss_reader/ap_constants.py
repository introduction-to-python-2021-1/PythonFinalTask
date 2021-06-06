"""All constants used in the application."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

    from ap_rss_reader.ap_typing import HelloWorld

DUMP_FILE: Final[str] = "ap-rss-reader-dump.json"
HELLO_WORLD: Final[HelloWorld] = "Hello, World!"
TITLE: Final[str] = "AP RSS-reader"
