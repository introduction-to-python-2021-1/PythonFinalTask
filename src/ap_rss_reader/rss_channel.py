"""RSS Channel class."""

from __future__ import annotations

from datetime import datetime
from itertools import chain
import json
import os
from pathlib import Path
import re
from typing import cast
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup  # type: ignore
import requests
from requests import Response
from xhtml2pdf import pisa  # type: ignore

from ap_rss_reader import ap_constants as const
from ap_rss_reader import utils
from ap_rss_reader.ap_collections import Media
from ap_rss_reader.ap_typing import Article
from ap_rss_reader.log import logger

if TYPE_CHECKING:
    from typing import Any
    from typing import Dict
    from typing import Final
    from typing import List
    from typing import Optional
    from typing import Tuple

__all__ = ("get_rss_channel", "RssChannel")


def get_rss_channel(  # noqa: C901
    url: Optional[str] = None, limit: int = 0, date: Optional[str] = None
) -> Optional[RssChannel]:
    """Check arguments and return RssChannel instance if no errors.

    Args:
        url:  Url of rss channel.
        limit:  Max count of displayed articles.
        date:  Articles before given date will be hidden.

    Returns:
        RssChannel instance when all parameters are correct, `None`
            otherwise.

    """
    if not date and not url:
        logger.info(const.DATE_OR_SOURCE_IS_REQUIRED)
        return None

    if limit and (
        not isinstance(limit, int) or (isinstance(limit, int) and limit < 0)
    ):
        logger.info(
            "'limit' must be number and greater than 0. "
            "Or equal to 0 if there is no limit."
        )
        return None

    limit_date: Optional[datetime] = None
    if date:
        try:
            limit_date = datetime.strptime(date, "%Y%m%d")
        except (TypeError, ValueError):
            logger.info(
                "The 'date' argument must be string and match format '%Y%m%d'."
            )
            return None

    if url and not utils.validate_url(url):
        logger.info(const.ERROR_INCORRECT_SOURCE_ARG, {"url": url})
        return None

    logger.debug("\nCreate rss-channel instance.")
    rss_channel = RssChannel(url=url, limit=limit, date=limit_date)
    logger.debug("\nLoad data...")
    rss_channel.load()
    logger.debug(const.INFO_CHANNEL_WAS_CREATED, {"count": len(rss_channel)})
    return rss_channel


class RssChannel:
    """RssChannel class specifies the public methods of rss."""

    SELECTOR: Final[str] = "rss channel"
    ARTICLE_SELECTOR: Final[str] = "item"

    def __init__(
        self,
        *,
        url: Optional[str] = None,
        limit: int = 0,
        date: Optional[datetime] = None,
    ):
        """Create new rss channel.

        Args:
            url:  Url of rss channel.  When `url` is not given, try to
                read data from file.
            limit:  Max count of displayed articles.  0 - when there's
                no limits.
            date: Only articles after given date will be displayed.  If
                date passed, articles are loaded from file.

        """
        self._limit = limit or 0
        self._articles: List[Article] = []
        self._title: str = ""
        self._description: str = ""
        self._url: str = url or ""
        self._date: Optional[datetime] = date

    def __len__(self) -> int:
        return len(self._articles)

    def __getitem__(self, index: int) -> Optional[Article]:
        """Return Article by index."""
        return self._articles[index]

    def __bool__(self) -> bool:
        return bool(self._title or self._url)

    @property
    def url(self) -> str:
        """Url of rss channel."""
        return self._url

    @property
    def limit(self) -> int:
        """The max count of displayed articles."""
        return self._limit

    @limit.setter
    def limit(self, limit: int) -> None:
        """Set new limit."""
        if isinstance(limit, int) and limit >= 0:
            self._limit = limit

    @property
    def articles(self) -> List[Article]:
        """All articles."""
        return self._articles[: self._limit] if self._limit else self._articles

    @property
    def articles_by_date(self) -> List[Article]:
        """Articles are published after :attr:`date`."""
        articles = (
            list(
                filter(
                    lambda article: cast(  # type: ignore
                        datetime, article[const.FIELD_PUBDATE]
                    )
                    >= self._date,
                    self._articles,
                )
            )
            if self._date
            else self.articles
        )

        return articles[: self._limit] if self._limit else articles

    @property
    def title(self) -> str:
        """Title of rss channel."""
        return self._title

    @property
    def html(self) -> str:
        """Rss channel as html representation."""
        return const.HTML_TEMPLATE.format(
            title=self._title,
            url=self._url,
            description=self._description,
            body="<br>".join(
                utils.article2html(article)
                for article in self.articles_by_date
            ),
        )

    def save_pdf(self, filename: str) -> Any:
        """Saved rss channel to pdf file.

        Args:
            filename: name of pdf file where data will be saved.

        """
        try:
            logger.debug(f"Open file {filename}...")
            with open(filename, "w+b") as f:
                pisa.CreatePDF(src=self.html, dest=f)
            logger.debug("Close file.")
        except OSError:
            logger.info(const.ERROR_OPEN_FILE, {"filename": filename})

    def load(self) -> None:
        """Load articles from file or Internet using 'url'."""
        if self._date:
            self.read()
        else:
            self.fetch()
            self.dump()

    def print(self) -> None:
        """Print channel title and limited article list."""
        self._print_feed_title()
        if articles := self.articles_by_date:
            for article in articles:
                logger.info("\n")
                utils.print_article(article)
        else:
            logger.info("There's no data!")

    def json(self, *, whole: bool = False) -> str:
        """Convert `Channel` to json.

        Args:
            whole: If `True`, return the RSS channel and all articles as
                JSON.  Otherwise, return only articles limited by
                :attr:`limit` property.

        Returns:
            Rss channel as json.

        """
        return json.dumps(self._serialize(whole), indent=4, sort_keys=True)

    def dump(self, file: str = "") -> None:
        """Write the rss channel on the file (as JSON).

        Args:
            file: filename where data will be saved.

        """
        logger.debug("\nDump data to file.")

        if not self._url:
            logger.info(
                "Data cannot be saved to file, due to missing rss-channel url."
            )
            return

        full_path, data = self._read_file(file)
        with open(full_path, "w") as df:
            current_channel: Dict[str, Any] = next(
                filter(lambda channel: channel["url"] == self._url, data),
                None,  # type: ignore
            )
            if current_channel:
                # Convert articles from file and from instance to dict
                # with "title" as unique key.  Replace old articles
                # (from file) with articles from instance
                serialized_articles: List[Dict[str, Any]] = list(
                    {
                        **{
                            article[const.FIELD_TITLE]: article
                            for article in current_channel["articles"]
                        },
                        **{
                            article[const.FIELD_TITLE]: article
                            for article in self._serialize()["articles"]
                        },
                    }.values()
                )
                # update current rss channel using "url" as key
                data = [
                    dict(
                        title=self._title,
                        url=self._url,
                        description=self._description,
                        articles=serialized_articles,
                    )
                    if channel["url"] == self._url
                    else channel
                    for channel in data
                ]
            else:
                data.append(self._serialize())
            json.dump(
                data,
                df,
                indent=4,
                sort_keys=True,
            )

    def fetch(self) -> None:
        """Fetch and parse data using url."""
        logger.debug(f"\nFetch data with {self._url}...")

        content = self._request()
        # lxml doesn't support pseudo-classes. So we fix it:
        content = self._fix_pseudo_classes(content)
        beautiful_soup = self._get_beautiful_soup(content)

        if beautiful_soup and (
            feed_title := utils.retrieve_title(beautiful_soup)
        ):
            self._title = feed_title
            description = beautiful_soup.select_one("description")
            self._description = description.string if description else None
            articles = beautiful_soup.select(self.ARTICLE_SELECTOR)
            logger.debug(f"\n{len(articles)} was(were) downloaded.")
            self._articles = [
                utils.parse_article(article)
                for article in articles
                if utils.retrieve_title(article)
            ]
        else:
            logger.info(const.ERROR_NO_DATA)

    def read(self, filename: str = "") -> None:
        """Read the rss channel from the JSON file.

        When there's no saved url in :attr:`_url`, read *all* articles
        from *all* channels in file.

        Args:
            filename: name of file from which attempts to read data.

        """
        logger.debug("\nLoad rss-channel from file...")

        serialized_articles: List[Dict[str, Any]]

        _, data = self._read_file(filename)
        if self._url:
            serialized_channel: Dict[str, Any] = next(
                filter(lambda channel: channel["url"] == self._url, data),
                None,  # type: ignore
            )
            if serialized_channel:
                self._title = serialized_channel["title"]
                self._description = serialized_channel["description"]
                serialized_articles = serialized_channel["articles"]
            else:
                serialized_articles = []
        else:
            # Read *all* articles from *all* feeds in file
            serialized_articles = list(
                chain.from_iterable([channel["articles"] for channel in data])
            )

        articles: List[Article] = []
        for serialized_article in serialized_articles:
            article = serialized_article
            if const.FIELD_PUBDATE in article:
                article[const.FIELD_PUBDATE] = datetime.strptime(
                    article[const.FIELD_PUBDATE], const.DATETIME_FORMAT
                )
            if const.FIELD_MEDIA in article:
                article[const.FIELD_MEDIA] = [
                    Media(*media) for media in article[const.FIELD_MEDIA]
                ]
            articles.append(cast(Article, article))
        self._articles = articles

    @classmethod
    def _get_beautiful_soup(cls, content: str) -> BeautifulSoup:
        """Convert content to soup and return rss channel.

        Args:
            content: text with xml formatted rss channel.

        Returns:
            Content of rss channel as soup.

        """
        return BeautifulSoup(content, features="lxml").select_one(cls.SELECTOR)

    def _request(self) -> str:  # noqa: C901
        """Send request and return response as text.

        Returns:
            Text of rss feed.

        """
        if not self._url:
            logger.info(const.ERROR_NO_URL)
            return ""

        try:
            logger.debug(f"Send request to {self._url}...")
            response: Response = requests.request(
                "GET", self._url, timeout=(3.0, 5.0)
            )
            if not response:
                response.raise_for_status()
        except requests.HTTPError as e:
            status_code = e.response.status_code
            logger.info(
                const.REQUEST_ERROR_MESSAGES.get(
                    status_code,
                    " ".join(
                        (const.ERROR_SOMETHING_GOES_WRONG, const.ERROR_CODE)
                    ),
                ).format(code=status_code, url=self._url)
            )
        except requests.ConnectionError as e:
            host: str = f": {e.args[0].pool.host}" if "pool" in e.args else ""
            logger.info(const.ERROR_NO_ADDRESS, {"host": host})
        except requests.ReadTimeout as e:
            host = f": {e.args[0].pool.host}" if "pool" in e.args else ""
            logger.info(const.ERROR_TIME_OUT, {"host": host})
        except requests.TooManyRedirects:
            logger.info(const.ERROR_TOO_MANY_REDIRECTS)
        except requests.exceptions.ContentDecodingError:
            logger.info(const.ERROR_FAILED_DECODE)
        except requests.RequestException:
            logger.info(const.ERROR_SOMETHING_GOES_WRONG)
        else:
            return response.text
        return ""

    def _print_feed_title(self) -> None:
        """Print title and url current rss feed if data exists."""
        if self._title:
            logger.info(f"\n\nFeed: {self._title}")
        if self._url:
            logger.info(f"Url: {self._url}")
        if self._description:
            logger.info(f"Description: {self._description}\n")

    def _serialize(self, whole: bool = True) -> Dict[str, Any]:
        """Represent RssChannel using python primitive types.

        Args:
            whole: If `True`, return the RSS channel and all articles as
                JSON.  Otherwise, return only articles limited by
                :attr:`limit` property.

        Returns:
            Rss channel as :obj:`dict` object.

        """
        articles = self._articles if whole else self.articles_by_date
        return dict(
            title=self._title,
            url=self._url,
            description=self._description,
            articles=[
                {
                    **article,
                    const.FIELD_PUBDATE: cast(
                        datetime, article[const.FIELD_PUBDATE]
                    ).strftime(const.DATETIME_FORMAT),
                }
                for article in articles
                if isinstance(article[const.FIELD_PUBDATE], datetime)
            ],
        )

    @classmethod
    def _read_file(cls, filename: str) -> Tuple[Path, List[Dict[str, Any]]]:
        """Read json-data from file.

        Args:
            filename: name of file from which data will be read.

        Returns:
            Tuple with two items: full path to file and json-data.

        """
        full_path: Path = cls._get_full_path(filename)
        data: List[Dict[str, Any]] = []
        if os.path.isfile(full_path):
            with open(full_path) as fr:
                logger.debug(f"\nRead data from file as json ({full_path}).")
                try:
                    data = json.load(fr)
                except ValueError:
                    logger.info(const.ERROR_JSON_LOAD)
        return full_path, data

    @staticmethod
    def _get_full_path(filename: str = "") -> Path:
        """Build full path with given `file` and return :obj:`Path`.

        Args:
            filename: name of file from which data will be read.

        Returns:
            Full path to file.

        """
        if not filename:
            filename = (
                os.environ.get("AP_RSS_READER_DUMP_FILE") or const.DUMP_FILE
            )
        base_dir: Path = Path(__file__).parent.resolve(strict=True)
        full_path: Path = base_dir / filename
        if os.path.isfile(full_path):
            logger.debug(f"\nDump file already exists ({full_path})!")
        return full_path

    @staticmethod
    def _fix_pseudo_classes(text: str) -> str:
        """Replace ':' in pseudo classes with '_'.

        Args:
            text: Text that will be parsed.

        Returns:
            Text with replaced pseudo classes.

        """
        return re.sub(
            "<(?P<tag>[a-z]+):(?P<pseudo_class>[a-z]+)",
            r"<\g<tag>_\g<pseudo_class>",
            text,
        )
