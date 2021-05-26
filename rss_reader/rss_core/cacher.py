"""
    Contains class for working working with cache
"""
import calendar
import re
from abc import ABC, abstractmethod
from rss_core.rss_classes import RssNews, RssItem
from utils import util
from utils.db_processor import DbProcessor

MONTH_NUM = {month: index for index, month in enumerate(calendar.month_abbr)}


class Cacher(ABC):
    """
    Abstract class for setting cache classes
    """

    @abstractmethod
    def cache_rss_news(self, rss_news: RssNews, rss_link: str, show_logs: bool = False):
        """Create cache of RssNews object"""

    @abstractmethod
    def get_from_cache(self, rss_link: str, date: str = None, show_logs: bool = False):
        """Restore RssNews object from cache"""


class DbCacher(Cacher):
    """
    Class for working with cache
    """

    def __init__(self, db_name: str = ""):
        self.db_name = db_name
        self.db_processor = DbProcessor(self.db_name)
        self._create_tables()

    def _create_tables(self):
        """
        Set up db: create all necessary tables and indexes if they are not exist
        :return: None
        """
        query = """CREATE TABLE if NOT EXISTS "channels" (
                    "id"	INTEGER,
                    "rss_link"	TEXT NOT NULL DEFAULT '' UNIQUE,
                    "title"	TEXT NOT NULL DEFAULT '',
                    "link"	TEXT NOT NULL DEFAULT '',
                    "description"	TEXT NOT NULL DEFAULT '',
                    PRIMARY KEY("id" AUTOINCREMENT));"""
        self.db_processor.perform_query(query)

        query = """CREATE TABLE if NOT EXISTS "news" (
                            "id"	INTEGER,
                            "channel_id" INTEGER NOT NULL DEFAULT -1,
                            "guid" TEXT NOT NULL DEFAULT '',
                            "title"	TEXT NOT NULL DEFAULT '',
                            "link"	TEXT NOT NULL DEFAULT '' UNIQUE,
                            "short_date" DATE NOT NULL DEFAULT '0000-0-0',
                            "pub_date"	TEXT NOT NULL DEFAULT '',
                            "description"	TEXT NOT NULL DEFAULT '',
                            "category"	TEXT NOT NULL DEFAULT '',
                            PRIMARY KEY("id" AUTOINCREMENT));"""
        self.db_processor.perform_query(query)

        query = """CREATE INDEX IF NOT EXISTS news_by_bate ON news (channel_id ASC, short_date ASC);"""
        self.db_processor.perform_query(query)

        query = """CREATE TABLE if NOT EXISTS "content" (
                    "id"	INTEGER,
                    "news_id" INTEGER NOT NULL DEFAULT -1,
                    "link"	TEXT NOT NULL DEFAULT '',
                    PRIMARY KEY("id" AUTOINCREMENT));"""
        self.db_processor.perform_query(query)

        query = """CREATE INDEX IF NOT EXISTS content_by_news_id ON content (news_id ASC);"""
        self.db_processor.perform_query(query)

    def cache_rss_news(self, rss_news: RssNews, rss_link: str, show_logs: bool = False):
        """
        Create cache or news into db
        :param rss_news: Object of RssNews class with all required information for caching
        :param rss_link: link for getting rss news from chanel
        :param show_logs: show or hide logs
        :return: None
        """
        try:
            util.log(msg="Start creating cache...", flag="INFO", show_on_console=show_logs)
            channel_id = self._create_channel_cache(rss_link=rss_link, rss_news=rss_news)
            self._create_news_cache(channel_id=channel_id, rss_news=rss_news)
            util.log(msg="Nes was cached successfully", flag="INFO", show_on_console=show_logs)

        except LookupError as err:
            util.log(msg=f"Error has happened while caching: {str(err)}", flag="ERROR", show_on_console=True)

    def _create_channel_cache(self, rss_link: str, rss_news: RssNews):
        chanel_ids = self.db_processor.select(
            f"SELECT id FROM channels WHERE rss_link = '{rss_link}'")

        if not chanel_ids:
            self.db_processor.insert(table_name="channels",
                                     insert_values={"rss_link": rss_link, "title": rss_news.title,
                                                    "link": rss_news.link, "description": rss_news.description},
                                     ignore=False)

            chanel_ids = self.db_processor.select(f"SELECT id FROM channels WHERE rss_link = '{rss_link}'")
            if not chanel_ids:
                raise LookupError(f"Can't create cache for chanel {rss_link}")

        chanel_id = chanel_ids[0]['id']
        return chanel_id

    def _create_news_cache(self, channel_id: int, rss_news: RssNews):
        """
        Create cache of news items for channel with id = channel_id
        :param channel_id: id of channel in db
        :param rss_news: RssNews object, which contains news to be cached
        :return: None
        """
        for news_item in rss_news.news:
            simple_date = self._extract_date_from_string(news_item.pub_date)
            self.db_processor.insert(table_name="news",
                                     insert_values={"channel_id": channel_id, "guid": news_item.guid,
                                                    "title": news_item.title, "link": news_item.link,
                                                    "short_date": simple_date, "pub_date": news_item.pub_date,
                                                    "description": news_item.description,
                                                    "category": news_item.category}, ignore=True)

            news_ids = self.db_processor.select(f"SELECT id FROM news WHERE link = '{news_item.link}'")
            if not news_ids:
                raise LookupError(f"Can't create cache for news {str(news_item)}")

            news_id = news_ids[0]['id']
            self._create_content_cache(news_id=news_id, content_links=news_item.content)

    def _create_content_cache(self, news_id: int, content_links):
        """
        Create cache of content (media links) for news item with id = news_id
        :param news_id: id of news item in db
        :param content_links: array of links to be cached
        :return: None
        """
        for content in content_links:
            self.db_processor.insert(table_name="content",
                                     insert_values={"news_id": news_id, "link": content}, ignore=True)

    def _extract_date_from_string(self, pub_date: str):
        """
        Extract date and format to yyyy-mm-dd from
        different types of pub_date
        :param pub_date: timestamp in channel format
        :return: date in yyyy-mm-dd format
        """
        matches = re.findall(r"(\d{4})-0*(\d{1,2})-(\d{1,2})", pub_date)
        if matches:
            ok_date = f"{matches[0][0]}-{matches[0][1]}-{matches[0][2]}"
            return ok_date

        matches = re.findall(r"(\d{1,2})\s+(\w{3})\s+(\d{4})", pub_date)
        if matches:
            ok_date = f"{matches[0][2]}-{MONTH_NUM[matches[0][1]]}-{matches[0][0]}"
            return ok_date

        raise ValueError(f"Can't extract date from pub_date field: {pub_date}")

    def get_from_cache(self, rss_link: str, date: str = None, show_logs: bool = False):
        """
        Get rss news from cache
        :param rss_link: link for getting rss nes from chanel
        :param date: date of publishing news
        :param show_logs: whether we want to show logs
        :return: RssNews object
        """
        try:
            util.log(msg="Start getting news from cache", flag="INFO", show_on_console=show_logs)
            rss_news_dict = {}
            channel_info = self._get_channel_info_from_db(rss_link)
            channel_id = channel_info["id"]

            rss_news_dict["title"] = channel_info["title"]
            rss_news_dict["link"] = channel_info["link"]
            rss_news_dict["description"] = channel_info["description"]
            rss_news_dict["news"] = self._get_rss_news_from_db(channel_id, date)
            rss_news = RssNews(**rss_news_dict)
            util.log(msg="News was restored from cache", flag="INFO", show_on_console=show_logs)
            return rss_news
        except ValueError as err:
            util.log(msg=f"Value error has occurred while restoring news from cache: {str(err)}", flag="ERROR",
                     show_on_console=True)
            exit(1)
        except LookupError as err:
            util.log(msg=f"Lookup error has occurred while restoring news from cache: {str(err)}", flag="ERROR",
                     show_on_console=True)
            exit(1)

    def _get_rss_news_from_db(self, channel_id: int, date: str = None):
        """
        Restore news items from db for channel with id = channel id
        and for date. If date is None all news for channel will be shown
        :param channel_id: id of chanel in db
        :param date: date for selecting news
        :return: array of RssItem objects
        """
        news = []
        query = f"SELECT * FROM news WHERE channel_id ={channel_id}"
        if date:
            correct_date = self._cast_date_to_db_view(date)
            query += f" AND short_date = '{correct_date}'"
        news_info = self.db_processor.select(query)
        for news_item_info in news_info:
            news_id = news_item_info["id"]
            news_item_info["content"] = self._get_content_links_from_db(news_id=news_id)
            news_item_info["pubDate"] = news_item_info["pub_date"]
            news.append(RssItem(**news_item_info))
        return news

    def _get_content_links_from_db(self, news_id: int):
        """
        Restore content links from db for news item with id = news_id
        :param news_id: news item for want we want to get content
        :return: array od str (links)
        """
        content_info = self.db_processor.select(f"SELECT * FROM content WHERE news_id ={news_id} ")
        return [content_item["link"] for content_item in content_info]

    def _get_channel_info_from_db(self, rss_link: str):
        """
        Restore info about chanel from db
        :param rss_link: rss link for getting news from chanel
        :return: dict of info about chanel
        """
        channel_info = self.db_processor.select(
            f"SELECT id, title, link, description FROM channels WHERE rss_link ='{rss_link}'")

        if not channel_info:
            raise LookupError(f"Can't find cache for this chanel :{rss_link}")
        return channel_info[0]

    def _cast_date_to_db_view(self, date: str):
        """
        Cast date from %Y%m%d to %Y-%m-%d format
        :param date: input date in %Y%m%d format
        :return: str date in %Y-%m-%d format
        """
        if date.startswith("0"):
            raise ValueError(f"Can't parse date '{date}'. Date can't starts with 0")
        ymd = re.findall(r"^(\d{4})(\d{2})(\d{2})$", date)
        if not ymd:
            raise ValueError(f"Can't parse date '{date}'. Check if it is %Y%m%d format")
        correct_date = f"{ymd[0][0]}-{ymd[0][1]}-{ymd[0][2]}"
        correct_date = re.sub(r"-0", "-", correct_date)
        return correct_date
