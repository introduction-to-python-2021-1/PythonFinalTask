import json
import logging
import datetime
from pathlib import Path

import dateparser

try:
    from logger_config import get_logger
except ImportError:
    from .logger_config import get_logger

logger = get_logger()


class LocalStorage:
    """Implements local storage and interface to interact with it."""

    @staticmethod
    def parse_date_from_news_item(news_item):
        return dateparser.parse(news_item["Date"])

    def __init__(self, name):
        base = Path(__file__).resolve().parent.parent / "data"
        base.mkdir(exist_ok=True)
        jsonpath = base / f"{name}.json"
        jsonpath.touch(exist_ok=True)

        self.jsonpath = jsonpath

    def set_channel_by_url(self, url, news_items):
        # Sorts channel news items by date
        sorted_news_items = sorted(news_items, reverse=True, key=self.parse_date_from_news_item)

        storage_content = self.read_from_storage_file()

        if url in storage_content:
            # To prevent duplication of news items from the same url
            storage_has_news_items_by_url = bool(len(storage_content[url]))
            date_of_latest_news_item_by_url = self.parse_date_from_news_item(storage_content[url][0])
            i = 0

            while storage_has_news_items_by_url and i < len(sorted_news_items) and \
                    date_of_latest_news_item_by_url < self.parse_date_from_news_item(sorted_news_items[i]):
                i += 1

            storage_content[url] = sorted_news_items[:i] + storage_content[url]
        else:
            storage_content[url] = sorted_news_items

        self.write_to_storage_file(storage_content)

    def get_channel_by_url_and_date(self, url, pub_date):
        logger.info(f"Get channel from local storage by url: {url} and date: {pub_date}")
        storage_content = self.read_from_storage_file()
        pub_date = datetime.datetime.strptime(pub_date, "%Y%m%d")

        def get_news_items_by_specific_date(news_items):
            nonlocal news_items_by_specific_date
            tmp = list(filter(lambda item: self.parse_date_from_news_item(item).date() == pub_date.date(), news_items))
            if tmp:
                news_items_by_specific_date += tmp

        news_items_by_specific_date = []

        if url in storage_content:
            news_items = storage_content[url]
            get_news_items_by_specific_date(news_items)
        else:
            for news_items in storage_content.values():
                get_news_items_by_specific_date(news_items)

        return sorted(news_items_by_specific_date, reverse=True, key=self.parse_date_from_news_item)

    def get_number_of_news_items_by_url(self, url):
        storage_content = self.read_from_storage_file()

        if url in storage_content:
            return len(storage_content[url])
        else:
            return 0

    def read_from_storage_file(self):
        return json.loads(self.jsonpath.read_bytes().decode() or "{}")

    def write_to_storage_file(self, data):
        self.jsonpath.write_bytes(json.dumps(data, indent=4, ensure_ascii=False).encode("utf8"))
