import json
from pathlib import Path

from dateparser import parse


class LocalStorage:
    def __init__(self, name):
        base = Path(__file__).resolve().parent.parent / "data"
        base.mkdir(exist_ok=True)
        jsonpath = base / f"{name}.json"
        jsonpath.touch(exist_ok=True)

        self.jsonpath = jsonpath

    def set_channel_by_url(self, url, channel):
        storage_content = self.read_from_storage_file()

        if url in storage_content:
            pass
        else:
            storage_content[url] = channel

        self.write_to_storage_file(storage_content)

    def get_channel_by_url_and_date(self, url, date):
        pass

    def read_from_storage_file(self):
        return json.loads(self.jsonpath.read_text() or "{}")

    def write_to_storage_file(self, data):
        self.jsonpath.write_text(json.dumps(data, indent=4))


local_storage = LocalStorage("localstorage")
