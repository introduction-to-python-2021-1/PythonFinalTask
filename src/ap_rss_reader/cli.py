"""Single point of application run."""

from argparse import ArgumentParser
import logging
import sys
from typing import List
from typing import Optional

import ap_rss_reader
from ap_rss_reader.ap_constants import HELLO_WORLD
from ap_rss_reader.ap_constants import TITLE
from ap_rss_reader.log import logger

__all__ = ("main", "create_parser")

if sys.version_info < (3, 8):
    raise RuntimeError("This package requires Python 3.8+!")


def create_parser() -> ArgumentParser:
    """Create argument parser, add arguments and return it."""
    parser = ArgumentParser(description=f"{TITLE} with CLI.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Provides additional details as to what the program is doing",
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Shows the version of the program and exits",
        version=f"{TITLE} {ap_rss_reader.__version__}",
    )
    return parser


def main(arguments: Optional[List[str]] = None) -> None:
    """Show message and exit."""
    if arguments is None:
        if len(sys.argv) <= 1:
            logger.info(HELLO_WORLD)
        arguments = sys.argv[1:]

    if len(arguments):
        args = create_parser().parse_args(arguments)

        if args.verbose:
            logger.setLevel(logging.DEBUG)
