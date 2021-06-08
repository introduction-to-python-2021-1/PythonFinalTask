import json
from pathlib import Path

import dateparser

ROOT_DIR = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT_DIR / "storage" / "storage.json"
CACHE_PATH.touch(exist_ok=True)


class Cache:
    def __init__(self, logger):
        CACHE_PATH.touch(exist_ok=True)
        self.storage = CACHE_PATH
        self.logger = logger

    def write_news(self, source, news_list):
        content = self.read_news()

        if content.get(source):
            fresh_news_list = self.eliminate_duplicates(content[source], news_list)
            content[source] = fresh_news_list
        else:
            content[source] = news_list

        with open(self.storage, "w") as fp:
            fp.write(json.dumps(content, indent=2, ensure_ascii=False))

    def read_news(self):
        with open(self.storage, "r") as fp:
            content = json.loads(fp.read() or "{}")
        return content

    def get_news_by_date(self, date_arg, source):
        content = self.read_news()
        initial_list = []
        news_for_specified_date = None
        if date_arg and source:
            news_for_specified_date = self.sort_by_date(
                initial_list, content[source], date_arg
            )
        else:
            for link, news in content.items():
                news_for_specified_date = self.sort_by_date(
                    initial_list, news, date_arg
                )
        if not news_for_specified_date:
            self.logger.error("No data for specified date")
        return news_for_specified_date

    @staticmethod
    def sort_by_date(news_for_specified_date, news_list, date_arg):
        for item in news_list:
            if dateparser.parse(item["Date"]).date() == date_arg.date():
                news_for_specified_date.append(item)

        return news_for_specified_date

    @staticmethod
    def eliminate_duplicates(caching_news_list, news_list_from_request):
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
