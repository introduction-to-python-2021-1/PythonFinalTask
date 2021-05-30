"""All constants used in the application."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

    from ap_rss_reader.ap_typing import HelloWorld

HELLO_WORLD: Final[HelloWorld] = "Hello, World!"
TITLE: Final[str] = "AP RSS-reader"
CHANNEL_SELECTOR: Final[str] = "rss channel"
CHANNEL_ITEM_SELECTOR: Final[str] = "item"
