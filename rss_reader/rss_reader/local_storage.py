import json
from pathlib import Path

import dateparser


class LocalStorage:
    def __init__(self, name):
        base = Path(__file__).resolve().parent.parent / "data"
        base.mkdir(exist_ok=True)
        jsonpath = base / f"{name}.json"
        jsonpath.touch(exist_ok=True)

        self.jsonpath = jsonpath

    def set_channel_by_url(self, url, channel):
        def parse_date_from_news_item(news_item):
            return dateparser.parse(news_item["Date"])
        # Sorts channel news items by date
        # Changes input dictionary "channel", not creates a copy of it
        channel["Items"] = sorted(channel["Items"], reverse=True, key=parse_date_from_news_item)

        storage_content = self.read_from_storage_file()

        if url in storage_content:
            # To prevent duplication of news items from the same url
            i = 0
            tmp_list = []
            storage_content_has_news_items = bool(len(storage_content[url]["Items"]))
            date_of_latest_news_item_in_storage_content = parse_date_from_news_item(storage_content[url]["Items"][0])

            while i < len(channel["Items"]) and storage_content_has_news_items and \
                    parse_date_from_news_item(channel["Items"][i]) > date_of_latest_news_item_in_storage_content:

                tmp_list.append(channel["Items"][i])
                i += 1

            storage_content[url]["Items"] = tmp_list + storage_content[url]["Items"]
        else:
            storage_content[url] = channel

        self.write_to_storage_file(storage_content)

    def get_channel_by_url_and_date(self, url, date):
        pass

    def read_from_storage_file(self):
        return json.loads(self.jsonpath.read_text() or "{}")

    def write_to_storage_file(self, data):
        self.jsonpath.write_text(json.dumps(data, indent=4))
