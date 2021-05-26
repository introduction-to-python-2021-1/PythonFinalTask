import sys
import json
import logging
import datetime
import pkg_resources
from pathlib import Path
import concurrent.futures
from urllib.request import urlretrieve

import dateparser

from rss_reader.helper import get_path_to_data
from rss_reader.logger_config import get_logger

logger = get_logger()


class LocalStorage:
    """Implements local storage and interface to interact with it."""

    def __init__(self, name):
        logger.info(f'Create local storage "{name}"')

        storagepath = Path(get_path_to_data("json", f"{name}.json"))
        storagepath.touch(exist_ok=True)

        self.storagepath = storagepath

    def set_news_items_by_url(self, url, news_items):
        """
        Sets news items to local storage by specific url and returns them, items are sorted so latest news comes first.

        Parameters:
            url (str): URL by which save news items to local storage
            news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}]: [] of {}'s

        Returns:
            [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}]: Sorted list of dicts
        """
        # Sorts channel news items by date, latest news comes first
        news_items_sorted_by_date = sorted(news_items, reverse=True, key=self.parse_date_from_news_item)
        storage_content = self.read_from_storage_file()

        if url in storage_content:
            # To prevent duplication of news items from the same url
            storage_has_news_items_by_url = bool(len(storage_content[url]))
            # News items in news_items_sorted_by_date list which index is less than max_index will be added to storage
            max_index = None

            if storage_has_news_items_by_url:

                date_of_latest_news_item_by_url = self.parse_date_from_news_item(storage_content[url][0])
                max_index = 0

                for news_item in news_items_sorted_by_date:
                    if self.parse_date_from_news_item(news_item) > date_of_latest_news_item_by_url:
                        max_index += 1

            news_items_to_be_add_to_storage = news_items_sorted_by_date[:max_index]

            logger.info(f"Set {len(news_items_to_be_add_to_storage)} fresh news items in local storage by url: {url}")

            self.get_news_items_images(news_items_to_be_add_to_storage)
            storage_content[url] = news_items_to_be_add_to_storage + storage_content[url]
        else:
            logger.info(f"Set {len(news_items_sorted_by_date)} fresh news items in local storage by url: {url}")

            self.get_news_items_images(news_items_sorted_by_date)
            storage_content[url] = news_items_sorted_by_date

        self.write_to_storage_file(storage_content)
        self.get_number_of_news_items_by_url(url)

        return storage_content[url]

    def get_news_items_by_url_and_date(self, url, pub_date):
        """
        Returns news items by specific date or by specific url and date. Exits program if wrong date is provided.

        Parameters:
            url (None) or (str): URL to source from which return news items, if (None) from all sources
            pub_date (str): Date from which return news items

        Returns:
            [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}]: List of dicts
        """
        try:
            pub_date = datetime.datetime.strptime(pub_date, "%Y%m%d")
        except ValueError:
            logger.error("You entered wrong date")
            sys.exit()

        logger.info(
            "Get news items from local storage by" + (f" url: {url} and " if url else " ") + f"date: {pub_date.date()}"
        )

        def fold_news_items_by_url_and_date(news_items, news_items_by_specific_date):
            """Folds news items get by specific date to list news_items_by_specific_date."""

            tmp = [item for item in news_items if self.parse_date_from_news_item(item).date() == pub_date.date()]

            if tmp:
                news_items_by_specific_date += tmp

        news_items_by_specific_date = []
        storage_content = self.read_from_storage_file()

        if url in storage_content:
            news_items = storage_content[url]
            fold_news_items_by_url_and_date(news_items, news_items_by_specific_date)
        else:
            for news_items in storage_content.values():
                fold_news_items_by_url_and_date(news_items, news_items_by_specific_date)
        # Latest news comes first
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
        result = len(storage_content[url]) if url in storage_content else 0

        logger.info(f"There are {result} news items in local storage by url: {url}")

        return result

    def read_from_storage_file(self):
        """Returns dictionary containing local storage content or empty dictionary if local storage is empty."""
        return json.loads(self.storagepath.read_bytes().decode() or "{}")

    def write_to_storage_file(self, storage_content):
        """Writes dictionary containing local storage content to file as JSON."""
        self.storagepath.write_bytes(json.dumps(storage_content, indent=4, ensure_ascii=False).encode("UTF-8"))

    @staticmethod
    def parse_date_from_news_item(news_item):
        """
        Returns date from single news item.

        Parameters:
            news_item {"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}: News item dict

        Returns:
            (datetime.datetime): Date from news item dict by key "Date"
        """
        return dateparser.parse(news_item["Date"])

    @staticmethod
    def get_news_items_images(news_items):
        """
        Downloads news items images to ./project_data/images directory.

        Parameters:
            news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}]: [] of {}'s
        """
        logger.info("Download images")

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(news_items) or None)

        for news_item in news_items:
            url = news_item["image_url"]

            if url is not None:
                storage_path_on_local_machine = get_path_to_data("images", url.split("/")[-1] + ".jpg")
                news_item["image_url"] = storage_path_on_local_machine
                executor.submit(urlretrieve, url, storage_path_on_local_machine)
        # If wait in line below set to False, news is printed to stdout without waiting for all images to be downloaded
        # it can affect PDF generation (some images may be absent)
        executor.shutdown(wait=True)
