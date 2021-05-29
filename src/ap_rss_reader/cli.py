"""Single point of application run."""

import sys

from ap_rss_reader.ap_constants import HELLO_WORLD
from ap_rss_reader.log import logger

__all__ = ("main",)

if sys.version_info < (3, 8):
    raise RuntimeError("This package requires Python 3.8+!")


def main() -> None:
    """Show message and exit."""
    logger.info(HELLO_WORLD)
