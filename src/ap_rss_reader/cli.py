"""Single point of application run."""
from argparse import ArgumentParser
from datetime import datetime
import json
import logging
import re
import sys
from typing import Dict
from typing import List
from typing import Optional

from bs4 import BeautifulSoup  # type: ignore
import requests
from requests import Response

import ap_rss_reader
from ap_rss_reader.ap_collections import Channel
from ap_rss_reader.ap_collections import ChannelItem
from ap_rss_reader.ap_constants import CHANNEL_ITEM_SELECTOR
from ap_rss_reader.ap_constants import CHANNEL_SELECTOR
from ap_rss_reader.ap_constants import HELLO_WORLD
from ap_rss_reader.ap_constants import TITLE
from ap_rss_reader.ap_typing import ChannelAsDict
from ap_rss_reader.log import logger

__all__ = ("main", "create_parser", "get_beautiful_soup")

if sys.version_info < (3, 8):
    raise RuntimeError("This package requires Python 3.8+!")

_cached_content: Dict[str, BeautifulSoup] = dict()


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


def get_beautiful_soup(url: str) -> BeautifulSoup:
    """Download data on the first request.

    Save the downloaded page to the cache on the first request
    and return data from the cash on subsequent calls.

    """
    if url not in _cached_content:
        response: Response = requests.request("GET", url, timeout=(3.0, 5.0))
        if response:
            # lxml doesn't support pseudo-classes. Fix it:
            content = re.sub(
                "<(?P<tag>[a-z]+):(?P<pseudo_class>[a-z]+)",
                r"<\g<tag>_\g<pseudo_class>",
                response.text,
            )
            _cached_content[url] = BeautifulSoup(content, features="lxml")
        else:
            response.raise_for_status()
    return _cached_content[url]


def load_channel(url: str, limit: int = 0) -> Channel:
    """Request rss with url and parse it.

    Args:
        url (str): url of rss feed.
        limit (int): max count of news.

    Returns:
        :obj:`Channel`: RSS channel.

    """
    rss_channel: BeautifulSoup = get_beautiful_soup(url).select_one(
        CHANNEL_SELECTOR
    )
    rss_items = rss_channel.select(CHANNEL_ITEM_SELECTOR)
    if limit:
        rss_items = rss_items[:limit]

    channel = Channel(title=rss_channel.select_one("title").string, items=[])
    for rss_item in rss_items:
        channel.items.append(
            ChannelItem(
                title=rss_item.title.string,
                link=rss_item.link.next,
                date=datetime.strptime(
                    rss_item.pubdate.string, "%Y-%m-%dT%H:%M:%SZ"
                ),
                source=rss_item.source.string,
                source_url=rss_item.source["url"],
                media_content_url=rss_item.media_content["url"],
            )
        )
    return channel


def convert_channel_to_dict(channel: Channel) -> ChannelAsDict:
    """Convert `Channel` to dict.

    Args:
        channel (Channel): RSS channel.

    Returns:
        :obj:`dict`: channel as dictionary with predefined fields.

    """
    return ChannelAsDict(
        title=channel.title,
        items=[
            {
                "title": item.title,
                "link": item.link,
                "date": item.date.strftime("%Y-%m-%d %H:%M:%S"),
                "source": item.source,
                "source_url": item.source_url,
                "media_content_url": item.media_content_url,
            }
            for item in channel.items
        ],
    )


def print_news(channel: Channel) -> None:
    """Print channel title and all items from channel.

    Args:
        channel (Channel): rss channel

    """
    logger.info(f"\n{channel.title}\n")
    for item in channel.items:
        logger.info(
            f"Title: {item.title}\n"
            f"Date: {item.date}\n"
            f"Link: {item.link}\n"
        )
        if item.media_content_url or item.source_url:
            logger.info("Links:")
            counter = 0
            if item.source_url:
                counter += 1
                logger.info(
                    f'[{counter}]: {item.source_url} "{item.source}" (link)'
                )
            if item.media_content_url:
                counter += 1
                logger.info(f"[{counter}]: {item.media_content_url} (image)")
            logger.info("\n")


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

    channel = load_channel(url=args.source, limit=args.limit)
    if args.json:
        logger.info(
            json.dumps(
                convert_channel_to_dict(channel), indent=4, sort_keys=True
            )
        )
    else:
        print_news(channel)
