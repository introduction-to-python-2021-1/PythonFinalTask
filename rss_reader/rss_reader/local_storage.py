import json
from itertools import islice
from datetime import datetime

import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)


# this class open local storage file news.json in rss_reader/tmp/
# class storage news and deal output in console
class local_storage:
    # in __init__ we load news from storage in list
    def __init__(self, path="../tmp/news.json"):
        with open(path) as file:
            self.news_from_storage = json.load(file)
            with open(path) as file:
                self.news_from_storage = json.load(file)

    # return news by date in list
    def get_news_by_date_from_locale_storage(self, date, limit=50):
        news_by_date = []

        for i, item in enumerate(self.news_from_storage):
            item_date = datetime.strptime(item["Date"], "%Y-%m-%dT%H:%M:%SZ")
            item_date = item_date.replace(hour=0, minute=0, second=0)

            if item_date == datetime.strptime(date, "%Y%m%d"):
                news_by_date.append({
                    "Title": item["Title"],
                    "Date": item["Date"],
                    "Link": item["Link"],
                })
        return news_by_date[:limit]

    # method print news by date
    def print_news_from_storage_by_date(self, date, limit=50):
        count = 1
        for item in islice(self.get_news_by_date_from_locale_storage(date, limit), 0, limit):
            print(f"\n {count}")
            count += 1
            for key, value in item.items():
                print(f"{key}: {value}")

    # method print news by date in json format
    def print_news_from_storage_by_date_json_format(self, date, limit=50):
        json_formatted_list = json.dumps(self.get_news_by_date_from_locale_storage(date), indent=4, ensure_ascii=False)
        print(json_formatted_list)