"""Single point of application run."""
from argparse import ArgumentParser
from argparse import Namespace
from datetime import datetime
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

    parser.add_argument("source", nargs="?", type=str, help="RSS URL")
    parser.add_argument(
        "--date",
        type=str,
        help="Limit news topics by publishing date: YYYYMMDD",
    )
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


def print_args(args: Namespace) -> None:
    """Print `args`."""
    logger.debug("Next args were passed:")
    for arg in vars(args):
        logger.debug(f"{arg}: {getattr(args, arg)}")


def main(arguments: Optional[List[str]] = None) -> None:
    """Show message and exit.

    Args:
        arguments: list of command line arguments.

    """
    if arguments is None:
        if len(sys.argv) <= 1:
            logger.info(HELLO_WORLD)
            return
        arguments = sys.argv[1:]

    args = create_parser().parse_args(arguments)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    print_args(args)

    channel = RssChannel(
        url=args.source, limit=args.limit, fetch=not args.date
    )
    logger.debug("\nData was loaded!")

    if args.date:
        publishing_date = datetime.strptime(args.date, "%Y%m%d")
        channel.print(filter_func=lambda item: item.date >= publishing_date)
    elif args.json:
        logger.info(channel.as_json())
    else:
        channel.print()


if __name__ == "__main__":
    main()
