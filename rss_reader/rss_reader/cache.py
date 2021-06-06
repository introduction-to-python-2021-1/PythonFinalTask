import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT_DIR / "cache" / "cache.json"
CACHE_PATH.touch(exist_ok=True)


class Cache:
    def __init__(self, logger):
        CACHE_PATH.touch(exist_ok=True)
        self.storage = CACHE_PATH
        self.logger = logger

    def write_news(self, source, news_list):
        content = self.read_news()

        if content.get(source):
            local_content = set(tuple(dict_item.items()) for dict_item in content[source])
            content_from_request = set(tuple(dict_item.items()) for dict_item in news_list)
            union_content = local_content | content_from_request
            fresh_news_list = []
            for item in union_content:
                item_info = dict()
                for key, value in item:
                    item_info[key] = value
                fresh_news_list.append(item_info)
            content[source] = fresh_news_list
        else:
            content[source] = news_list
        with open(self.storage, "w") as fp:
            fp.write(json.dumps(content, indent=2, ensure_ascii=False))

    def read_news(self):
        with open(self.storage, "r") as fp:
            content = json.loads(fp.read() or "{}")
        return content
