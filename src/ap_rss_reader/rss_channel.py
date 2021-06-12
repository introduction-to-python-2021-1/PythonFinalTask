"""RSS Channel class."""

from __future__ import annotations

from datetime import datetime
from itertools import chain
import json
import os
from pathlib import Path
import re
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup  # type: ignore
import requests
from requests import Response

from ap_rss_reader.ap_collections import Article
from ap_rss_reader.ap_constants import DUMP_FILE
from ap_rss_reader.ap_typing import Filter
from ap_rss_reader.log import logger

if TYPE_CHECKING:
    from typing import Any
    from typing import Dict
    from typing import Final
    from typing import List
    from typing import Optional
    from typing import Tuple

__all__ = ("RssChannel",)


class RssChannel:
    """RssChannel class specifies the public methods of rss."""

    SELECTOR: Final[str] = "rss channel"
    ARTICLE_SELECTOR: Final[str] = "item"

    def __init__(
        self, *, url: Optional[str] = None, limit: int = 0, fetch: bool = True
    ):
        """Create new rss channel and load all news with the given url.

        Args:
            url (str, optional): Url of rss channel. When `url` is not
                given, try to load data from file.
            limit (:obj:`int`, optional): Max count of displayed news.
                0 - if there's no limits.
            fetch (bool, optional): When `True` data will loaded using
                `url` argument.  Otherwise data will be read from file.
                `True` by default.

        """
        url = url or ""

        self._limit = limit
        self._articles: List[Article] = []
        self._title: str = ""
        self._url: str = url

        if fetch:
            if not url:
                raise ValueError(
                    "Using 'fetch' argument without 'url' is prohibited!"
                )

            logger.debug(f"\nCreate new rss-channel with url: {url}...")
            beautiful_soup = self._get_beautiful_soup()
            if beautiful_soup:
                self._title = beautiful_soup.select_one("title").string
                articles = beautiful_soup.select(self.ARTICLE_SELECTOR)
                self._articles.extend(
                    [
                        Article(
                            title=article.title.string,
                            link=article.link.next,
                            date=datetime.strptime(
                                article.pubdate.string,
                                "%Y-%m-%dT%H:%M:%SZ",
                            ),
                            source=article.source.string,
                            source_url=article.source
                            and article.source["url"],
                            media_content_url=article.media_content
                            and article.media_content["url"],
                        )
                        for article in articles
                    ]
                )
                self.dump()
        else:
            self._articles = self.load()

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
    def articles(self) -> List[Article]:
        """:obj:`list` of :obj:`Article`: All news."""
        return self._articles[: self._limit] if self._limit else self._articles

    @property
    def title(self) -> str:
        """str: Title of rss channel."""
        return self._title

    def print(self, *, filter_func: Optional[Filter] = None) -> None:
        """Print channel title and all channel items from channel."""
        self._print_feed_title()

        articles: List[Article] = (
            self.filter(filter_func) if filter_func else self.articles
        )
        if not articles:
            logger.info("There's no data!")

        self._print_articles(articles)

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
                url=self._url,
                articles=[
                    {
                        **article._asdict(),
                        "date": article.date.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for article in (self._articles if whole else self.articles)
                ],
            ),
            indent=4,
            sort_keys=True,
        )

    def dump(self, file: str = "") -> None:
        """Write the rss channel on the file (as JSON)."""
        full_path, data = self._read_file(file)

        if self._url:
            with open(full_path, "w") as df:
                current_channel: Dict[str, Any] = next(
                    filter(lambda channel: channel["url"] == self._url, data),
                    None,  # type: ignore
                )
                if current_channel is not None:
                    # Convert news from file and from instance to dict
                    # with "link" as unique key.  Replace old news (from
                    # file) with news from instance
                    all_news: List[Dict[str, Any]] = list(
                        {
                            **{
                                article["link"]: article
                                for article in current_channel["articles"]
                            },
                            **{
                                article.link: {
                                    **article._asdict(),
                                    "date": article.date.strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                }
                                for article in self._articles
                            },
                        }.values()
                    )
                    # replace current rss channel
                    data = [
                        dict(
                            title=self._title,
                            url=self._url,
                            articles=all_news,
                        )
                        if channel["url"] == self._url
                        else channel
                        for channel in data
                    ]
                else:
                    data.append(
                        dict(
                            title=self._title,
                            url=self._url,
                            articles=[
                                {
                                    **article._asdict(),
                                    "date": article.date.strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                }
                                for article in self._articles
                            ],
                        )
                    )
                json.dump(
                    data,
                    df,
                    indent=4,
                    sort_keys=True,
                )

    def load(self, file: str = "") -> List[Article]:
        """Read the rss channel from the JSON file."""
        logger.debug("\nLoad rss-channel from file...")
        _, data = self._read_file(file)

        all_news: List[Dict[str, Any]]
        if self._url:
            current_channel: Dict[str, Any] = next(
                filter(lambda channel: channel["url"] == self._url, data),
                None,  # type: ignore
            )
            if current_channel is not None:
                self._title = current_channel["title"]
                all_news = current_channel["articles"]
            else:
                all_news = []
        else:
            all_news = list(
                chain.from_iterable([channel["articles"] for channel in data])
            )
        return [
            Article(
                **{
                    **current_news,  # type: ignore
                    "date": datetime.strptime(
                        current_news["date"], "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )
            for current_news in all_news
        ]

    def filter(self, function: Filter, /) -> List[Article]:
        """Return news for witch `function` return `True`."""
        return list(filter(function, self._articles))

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

    def _print_feed_title(self) -> None:
        """Print title and url current rss feed if data exists."""
        if self._title:
            logger.info(f"\nFeed: {self._title}")
        if self._url:
            logger.info(f"Url: {self._url}\n")

    @classmethod
    def _read_file(cls, file: str) -> Tuple[Path, List[Dict[str, Any]]]:
        full_path: Path = cls._get_full_path(file)
        data: List[Dict[str, Any]] = []
        if os.path.isfile(full_path):
            with open(full_path) as fr:
                data = json.load(fr)
        return full_path, data

    @staticmethod
    def _get_full_path(file: str = "") -> Path:
        """Build full path with given `file` and return :obj:`Path`."""
        if not file:
            file = os.environ.get("AP_RSS_READER_DUMP_FILE") or DUMP_FILE
        base_dir: Path = Path(__file__).parent.resolve(strict=True)
        full_path: Path = base_dir / file
        if os.path.isfile(full_path):
            logger.debug(f"\nDump file already exists ({full_path})!")
        return full_path

    @staticmethod
    def _fix_pseudo_classes(text: str) -> str:
        """Replace ':' in pseudo classes with '_'."""
        return re.sub(
            "<(?P<tag>[a-z]+):(?P<pseudo_class>[a-z]+)",
            r"<\g<tag>_\g<pseudo_class>",
            text,
        )

    @staticmethod
    def _print_articles(articles: List[Article]) -> None:
        for article in articles:
            logger.info(
                f"Title: {article.title}\n"
                f"Date: {article.date}\n"
                f"Link: {article.link}\n"
            )
            if article.media_content_url or article.source_url:
                logger.info("Links:")
                counter = 0
                if article.source_url:
                    counter += 1
                    logger.info(
                        f"[{counter}]: {article.source_url} "
                        f'"{article.source}" (link)'
                    )
                if article.media_content_url:
                    counter += 1
                    logger.info(
                        f"[{counter}]: {article.media_content_url} " f"(image)"
                    )
                logger.info("\n")