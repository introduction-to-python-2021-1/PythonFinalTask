import json
import os
from pathlib import Path
import urllib.request
import dateparser
import hashlib
import imghdr

ROOT_DIR = Path(__file__).resolve().parent.parent


class Cache:
    """This class is used for implementing local storage"""

    def __init__(self, cache_dir, file_name, logger):
        """This method initialize local storage (includes image directory), receives logger object, cache folder and
        filename. """
        cache_path = ROOT_DIR / cache_dir / file_name
        cache_path.touch(exist_ok=True)
        image_storage = ROOT_DIR / cache_dir / "images"
        image_storage.mkdir(exist_ok=True)
        self.storage = cache_path
        self.image_storage = image_storage
        self.logger = logger

    def write_news(self, source, news_list):
        """This method eliminate duplicates, then write news in JSON format and save it in cache"""
        content = self.read_news()
        self.logger.info("Eliminating news duplicates...")
        if content.get(source):
            fresh_news_list = self.eliminate_duplicates(content[source], news_list)
            content[source] = fresh_news_list
        else:
            content[source] = news_list
        self.logger.info("Writing news to cache")
        with open(self.storage, "w") as fp:
            fp.write(json.dumps(content, indent=2, ensure_ascii=False))
        self.save_images(news_list)

    def read_news(self):
        """This method reads news from cache"""
        self.logger.info("Reading local storage...")
        with open(self.storage, "r") as fp:
            content = json.loads(fp.read() or "{}")
        return content

    def get_news_by_date(self, date_arg, source):
        """This method receives date and source, after sorting operation returns lst of news for specified date"""
        self.logger.info("Getting news from local storage...")
        content = self.read_news()
        news_for_specified_date = None
        if date_arg and source:
            news_for_specified_date = self.sort_by_date(content[source], date_arg)
        else:
            for link, news in content.items():
                news_for_specified_date = self.sort_by_date(news, date_arg)
        if not news_for_specified_date:
            self.logger.error("No data for specified date")
        return news_for_specified_date

    @staticmethod
    def sort_by_date(news_list, date_arg):
        """This method finds news for specified date"""
        news_for_specified_date = []
        for item in news_list:
            if dateparser.parse(item["Date"]).date() == date_arg.date():
                news_for_specified_date.append(item)

        return news_for_specified_date

    @staticmethod
    def eliminate_duplicates(caching_news_list, news_list_from_request):
        """This method eliminate duplicates: receives news from cache and news from request. Duplicates are
        eliminated with the use of sets"""
        local_content = set(tuple(dict_item.items()) for dict_item in caching_news_list)
        content_from_request = set(
            tuple(dict_item.items()) for dict_item in news_list_from_request
        )
        union_content = local_content | content_from_request
        fresh_news_list = []
        for item in union_content:
            item_info = dict()
            for key, value in item:
                item_info[key] = value
            fresh_news_list.append(item_info)

        return fresh_news_list

    def save_images(self, news_list):
        """This method saves images to local cache
        Filename is hash value of link to the img"""
        for item in news_list:
            if item.get("Image") is not None:
                img_path = (
                    self.image_storage
                    / f"{hashlib.md5(item.get('Image').encode()).hexdigest()}"
                )
                urllib.request.urlretrieve(item.get("Image"), img_path)
                img_format = imghdr.what(img_path)
                os.rename(img_path, f"{img_path}.{img_format}")
