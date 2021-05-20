import sys
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
        """
        Returns date from single news item.

                    Parameters:
                            news_item {"Feed": (str), "Title", (str), "Date": (srt), "Link": (str)}: News item dict

                    Returns:
                            (datetime.datetime): Date from news item dict by key "Date"
        """
        return dateparser.parse(news_item["Date"])

    def __init__(self, name):
        logger.info(f'Create local storage "{name}"')

        base = Path("../data")
        base.mkdir(exist_ok=True)
        jsonpath = base / f"{name}.json"
        jsonpath.touch(exist_ok=True)

        self.jsonpath = jsonpath

    def set_news_items_by_url(self, url, news_items):
        """
        Sets news items by specific url.

                    Parameters:
                            url (str): URL by which save news items to local storage
                            news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str)}]: List of dicts
        """
        # Sorts channel news items by date, latest news come first
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

            logger.info(f"Set {i} fresh news items in local storage by url: {url}")

            storage_content[url] = sorted_news_items[:i] + storage_content[url]
        else:
            logger.info(f"Set {len(sorted_news_items)} fresh news items in local storage by url: {url}")

            storage_content[url] = sorted_news_items

        self.write_to_storage_file(storage_content)

        self.get_number_of_news_items_by_url(url)

    def get_news_items_by_url_and_date(self, url, pub_date):
        """
        Returns news items by specific url and date.

                    Parameters:
                            url (None) or (str): URL to source from which return news items, if (None) from all sources
                            pub_date (str): Date from which return news items

                    Returns:
                            [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str)}]: List of dictionaries
        """
        logger.info(
            "Get news items from local storage by" + (f" url: {url} and " if url else " ") + f"date: {pub_date}"
        )

        try:
            pub_date = datetime.datetime.strptime(pub_date, "%Y%m%d")
        except ValueError:
            logger.error("You entered wrong date or not entered one at all")
            sys.exit()

        def fold_news_items_by_url_and_date(news_items):
            """Folds news items get by specific date to list named "news_items_by_specific_date"."""
            nonlocal news_items_by_specific_date

            tmp = list(filter(lambda item: self.parse_date_from_news_item(item).date() == pub_date.date(), news_items))

            if tmp:
                news_items_by_specific_date += tmp

        news_items_by_specific_date = []

        storage_content = self.read_from_storage_file()

        if url in storage_content:
            news_items = storage_content[url]
            fold_news_items_by_url_and_date(news_items)
        else:
            for news_items in storage_content.values():
                fold_news_items_by_url_and_date(news_items)
        # Latest news come first
        return sorted(news_items_by_specific_date, reverse=True, key=self.parse_date_from_news_item)

    def get_number_of_news_items_by_url(self, url):
        """
        Returns number of news items in local storage by specific url.

                    Parameters:
                            url (str): URL by which save news items to local storage

                    Returns:
                            result (int): Number of news items in local storage by specific url
        """
        storage_content = self.read_from_storage_file()

        if url in storage_content:
            result = len(storage_content[url])
        else:
            result = 0

        logger.info(f"There are {result} news items in local storage by url: {url}")

        return result

    def read_from_storage_file(self):
        """Returns dictionary containing local storage content or empty dictionary if local storage is empty."""
        return json.loads(self.jsonpath.read_bytes().decode() or "{}")

    def write_to_storage_file(self, storage_content):
        """Writes dictionary containing local storage content to file as JSON."""
        self.jsonpath.write_bytes(json.dumps(storage_content, indent=4, ensure_ascii=False).encode("UTF-8"))
