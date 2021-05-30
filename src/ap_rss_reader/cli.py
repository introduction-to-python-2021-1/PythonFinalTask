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
from ap_rss_reader.rss_channel import RssChannel

__all__ = ("main", "create_parser")

if sys.version_info < (3, 8):
    raise RuntimeError("This package requires Python 3.8+!")


def create_parser() -> ArgumentParser:
    """Create argument parser, add arguments and return it."""
    parser = ArgumentParser(description=f"{TITLE} with CLI.")

    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit news topics if this parameter provided",
    )
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
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print result as JSON in stdout",
    )
    return parser


def main(arguments: Optional[List[str]] = None) -> None:
    """Show message and exit.

    Args:
        arguments (:obj:`list` of :obj:`str`, optional): list of command
            line arguments.

    """
    if arguments is None:
        if len(sys.argv) <= 1:
            logger.info(HELLO_WORLD)
            return
        arguments = sys.argv[1:]

    args = create_parser().parse_args(arguments)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.debug("Next args were passed:")
    for arg in vars(args):
        logger.debug(f"{arg}: {getattr(args, arg)}")

    logger.debug(f"\nCreate new rss-channel {args.source}...")
    channel = RssChannel(url=args.source, limit=args.limit)
    logger.debug("\nData was loaded!")

    if args.json:
        logger.info(channel.as_json())
    else:
        channel.print()
