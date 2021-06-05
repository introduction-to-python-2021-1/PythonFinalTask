from itertools import islice
import json
from datetime import datetime

import rss_reader.channel_parser as channel_parser
import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)


# This class parses the site, handles data
# Outputs to stdout or file like .log or .json
class FeedContainer:
    def __init__(self, url):

        logger.info(f"Class {self.__class__.__name__}: initialization start.")

        self.root = channel_parser.get_response(url)
        self.__get_feed_info()

        logger.info(f"Class {self.__class__.__name__}: initialization done.")

    def __get_feed_info(self):
        logger.info(f"Class {self.__class__.__name__}: get all channel date.")
        self.__get_feed_title()
        self.__get_feed_description()
        self.__get_feed_link()
        self.__get_feed_date()
        self.__get_feed_copyright()
        self.__get_items()
        logger.info(
            f"Class {self.__class__.__name__}: data collection is done.")

    def __get_feed_title(self):
        self.feed_title = self.root.findtext("channel/title")

    def __get_feed_date(self):
        self.feed_date = self.root.findtext("channel/pubDate")

    def __get_feed_link(self):
        self.feed_link = self.root.findtext("channel/link")

    def __get_feed_description(self):
        self.feed_description = self.root.findtext("channel/description")

    def __get_feed_copyright(self):
        self.feed_copyright = self.root.findtext("channel/copyright")

    def __get_items(self):
        self.channel_items = []
        for i, item in enumerate(self.root.iterfind("channel/item")):
            self.channel_items.append({
                "Title": item.findtext("title"),
                "Date": item.findtext("pubDate"),
                "Link": item.findtext("link"),
            })

    def print_feed_Info(self):
        print(f"\nChannel title: {self.feed_title}",
              f"\nChannel link: {self.feed_link}"
              f"\nChannel description: {self.feed_description}"
              f"\nChannel date: {self.feed_date}"
              f"\nChannel copyright: {self.feed_copyright}")

    def print_news(self, limit=50):
        count = 1
        for item in islice(self.channel_items, 0, limit):
            print(f"\n {count}")
            count += 1
            for key, value in item.items():
                print(f"{key}: {value}")

    # 2021 - 06 - 04
    # T19: 08: 27Z
    def print_news_by_date(self, date, limit=50):
        news_by_date = []
        count = 1

        for i, item in enumerate(self.root.iterfind("channel/item")):
            item_date = datetime.strptime(item.findtext("pubDate"), "%Y-%m-%dT%H:%M:%SZ")
            item_date = item_date.replace(hour=0, minute=0, second=0)

            if item_date == datetime.strptime(date, "%Y%m%d"):
                news_by_date.append({
                    "Title": item.findtext("title"),
                    "Date": item.findtext("pubDate"),
                    "Link": item.findtext("link"),
                })

        for item in islice(news_by_date, 0, limit):
            print(f"\n {count}")
            count += 1
            for key, value in item.items():
                print(f"{key}: {value}")

    # this method return news
    def get_news(self, limit=50):
        return self.channel_items[:limit]

    def get_news_by_date(self, date, limit=50):
        news_by_date = []

        for i, item in enumerate(self.root.iterfind("channel/item")):
            item_date = datetime.strptime(item.findtext("pubDate"), "%Y-%m-%dT%H:%M:%SZ")
            item_date = item_date.replace(hour=0, minute=0, second=0)

            if item_date == datetime.strptime(date, "%Y%m%d"):
                news_by_date.append({
                    "Title": item.findtext("title"),
                    "Date": item.findtext("pubDate"),
                    "Link": item.findtext("link"),
                })
        return news_by_date[:limit]

    # this method saves news in json format
    def save_as_json(self, limit=50):
        with open("news.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(self.get_news(limit), indent=4, ensure_ascii=False))

    def save_as_json_by_date(self, date, limit=50):
        with open("news.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(self.get_news_by_date(date, limit), indent=4, ensure_ascii=False))
