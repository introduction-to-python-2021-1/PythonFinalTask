"""RSS Channel class."""

from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import re
from typing import Final
from typing import List

from bs4 import BeautifulSoup  # type: ignore
import requests
from requests import Response

from ap_rss_reader.ap_collections import ChannelItem
from ap_rss_reader.ap_constants import DUMP_FILE
from ap_rss_reader.log import logger

__all__ = ("RssChannel",)


class RssChannel:
    """RssChannel class specifies the public methods of rss."""

    SELECTOR: Final[str] = "rss channel"
    ITEM_SELECTOR: Final[str] = "item"

    def __init__(self, *, url: str, limit: int = 0):
        """Create new rss channel and load all news with the given url.

        Args:
            url (str): Url of rss channel.
            limit (:obj:`int`, optional): Max count of displayed news.
                0 - if there's no limits.

        """
        self._url = url
        self._limit = limit
        self._channel_items: List[ChannelItem] = []
        self._title = ""

        beautiful_soup = self._get_beautiful_soup()
        if beautiful_soup:
            self._title = beautiful_soup.select_one("title").string
            channel_items = beautiful_soup.select(self.ITEM_SELECTOR)
            self._channel_items.extend(
                [
                    ChannelItem(
                        title=channel_item.title.string,
                        link=channel_item.link.next,
                        date=datetime.strptime(
                            channel_item.pubdate.string, "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        source=channel_item.source.string,
                        source_url=channel_item.source
                        and channel_item.source["url"],
                        media_content_url=channel_item.media_content
                        and channel_item.media_content["url"],
                    )
                    for channel_item in channel_items
                ]
            )
            self.dump()

    @property
    def url(self) -> str:
        """str: url of rss channel."""
        return self._url

    @property
    def limit(self) -> int:
        """int: The max count of displayed news."""
        return self._limit

    @limit.setter
    def limit(self, limit: int) -> None:
        if isinstance(limit, int) and limit >= 0:
            self._limit = limit

    @property
    def channel_items(self) -> List[ChannelItem]:
        """:obj:`list` of :obj:`ChannelItem`: All news."""
        return (
            self._channel_items[: self._limit]
            if self._limit
            else self._channel_items
        )

    @property
    def title(self) -> str:
        """str: Title of rss channel."""
        return self._title

    def print(self) -> None:
        """Print channel title and all channel items from channel."""
        logger.info(f"\n{self._title}")
        logger.info(f"Url: {self._url}\n")
        for channel_item in self.channel_items:
            logger.info(
                f"Title: {channel_item.title}\n"
                f"Date: {channel_item.date}\n"
                f"Link: {channel_item.link}\n"
            )
            if channel_item.media_content_url or channel_item.source_url:
                logger.info("Links:")
                counter = 0
                if channel_item.source_url:
                    counter += 1
                    logger.info(
                        f"[{counter}]: {channel_item.source_url} "
                        f'"{channel_item.source}" (link)'
                    )
                if channel_item.media_content_url:
                    counter += 1
                    logger.info(
                        f"[{counter}]: {channel_item.media_content_url} "
                        f"(image)"
                    )
                logger.info("\n")

    def as_json(self, *, whole: bool = False) -> str:
        """Convert `Channel` to json.

        Args:
            whole (bool): If `True`, return the RSS channel and all news
                as JSON. Otherwise, return only news limited by `limit`
                property.  `False` by default.

        Returns:
            :obj:`str`: channel as json.

        """
        return json.dumps(
            dict(
                title=self._title,
                ulr=self._url,
                channel_items=[
                    {
                        "title": channel_item.title,
                        "link": channel_item.link,
                        "date": channel_item.date.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "source": channel_item.source,
                        "source_url": channel_item.source_url,
                        "media_content_url": channel_item.media_content_url,
                    }
                    for channel_item in (
                        self._channel_items if whole else self.channel_items
                    )
                ],
            ),
            indent=4,
            sort_keys=True,
        )

    def dump(self, file: str = "") -> None:
        """Write the rss channel on the file (as JSON)."""
        if not file:
            file = os.environ.get("AP_RSS_READER_DUMP_FILE") or DUMP_FILE
        base_dir: Path = Path(__file__).parent.resolve(strict=True)
        full_path: Path = base_dir / file
        if os.path.isfile(full_path):
            logger.debug(f"\nDump file will be re-written ({full_path}).")
        with open(full_path, "w") as df:
            df.write(self.as_json(whole=True))

    def _get_beautiful_soup(self) -> BeautifulSoup:
        """Download and convert data to beautiful soup.

        Returns:
            BeautifulSoup: content of rss channel.

        """
        response: Response = requests.request(
            "GET", self._url, timeout=(3.0, 5.0)
        )
        if not response:
            response.raise_for_status()
        # lxml doesn't support pseudo-classes. So we fix it:
        content = RssChannel._fix_pseudo_classes(response.text)
        beautiful_soup = BeautifulSoup(content, features="lxml").select_one(
            RssChannel.SELECTOR
        )
        return beautiful_soup

    @staticmethod
    def _fix_pseudo_classes(text: str) -> str:
        """Replace ':' in pseudo classes with '_'."""
        return re.sub(
            "<(?P<tag>[a-z]+):(?P<pseudo_class>[a-z]+)",
            r"<\g<tag>_\g<pseudo_class>",
            text,
        )
