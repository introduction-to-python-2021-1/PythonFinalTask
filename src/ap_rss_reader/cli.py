"""Single point of application run."""
from argparse import ArgumentParser
from argparse import Namespace
import logging
from pathlib import Path
import sys
from typing import List
from typing import Optional

import ap_rss_reader
from ap_rss_reader import ap_constants as const
from ap_rss_reader.log import logger
from ap_rss_reader.rss_channel import get_rss_channel

__all__ = ("main", "create_parser")

if sys.version_info < (3, 8):
    raise RuntimeError("This package requires Python 3.8+!")


def create_parser() -> ArgumentParser:
    """Create argument parser, add arguments and return it."""
    parser = ArgumentParser(description=f"{const.APP_TITLE} with CLI.")

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
        version=f"{const.APP_TITLE} {ap_rss_reader.__version__}",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print result as JSON in stdout",
    )
    parser.add_argument(
        "--to-html",
        type=str,
        help=(
            "Save rss channel as html file with given path:"
            r" 'C:\rss.html' or '/home/user/rss.html'."
        ),
    )
    parser.add_argument(
        "--to-pdf",
        type=str,
        help=(
            "Save rss channel as pdf file with given path:"
            r" 'C:\rss.html' or '/home/user/rss.html'."
        ),
    )
    return parser


def print_args(args: Namespace) -> None:
    """Print `args`."""
    logger.debug("Next args were passed:")
    for arg in vars(args):
        logger.debug(f"{arg}: {getattr(args, arg)}")


def get_sys_argv() -> List[str]:
    """Returns command-line arguments if they exist.

    Print help and exit if there are no arguments.

    """
    if len(sys.argv) <= 1:
        logger.info(const.GREETING)
    return sys.argv[1:]


def write_to_file(filename: str, text: str) -> None:
    """Write text to file with given filename.

    Args:
        filename: name of file where text will be written.
        text: text that will be written.

    """
    path: Path = Path(filename)
    if path.exists():
        logger.info(f"{filename} file exists and will be re-written!")

    try:
        logger.debug(f"Open file {filename}...")
        with path.open(mode="w") as f:
            f.write(text)
        logger.debug("Close file.")
    except OSError:
        logger.info(const.ERROR_OPEN_FILE, {"filename": filename})


def main(arguments: Optional[List[str]] = None) -> None:  # noqa: C901
    """The main public interface of application.

    Args:
        arguments: list of command line arguments.

    """
    parser = create_parser()
    args = parser.parse_args(arguments or get_sys_argv())

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    print_args(args)

    if not any(vars(args).values()):
        logger.info(parser.format_help())
        return

    channel = get_rss_channel(
        url=args.source, limit=args.limit, date=args.date
    )

    if channel is not None:
        filename: str
        if filename := args.to_html:
            write_to_file(filename, channel.html)
        if filename := args.to_pdf:
            channel.save_pdf(filename)

        if args.json:
            logger.info(channel.json())
        else:
            channel.print()
    else:
        logger.info(parser.format_help())


if __name__ == "__main__":
    main()
