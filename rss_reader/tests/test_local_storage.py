import ddt
import unittest

from rss_reader.local_storage import LocalStorage


@ddt.ddt
class TestGetNewsItemsByUrlAndDate(unittest.TestCase):
    """Tests get_news_items_by_url_and_date method of LocalStorage object with various arguments."""

    @classmethod
    def setUpClass(cls):
        cls.local_storage = LocalStorage("teststorage")

    @ddt.file_data("../project_data/json/teststoragedata.json")
    def test_get_news_items_by_url_and_date(self, url, pub_date, expected):
        """Tests get_news_items_by_url_and_date method of LocalStorage object with various arguments."""
        self.assertEqual(
            len(self.local_storage.get_news_items_by_url_and_date(url, pub_date)),
            expected,
            "Wrong output size"
        )


if __name__ == "__main__":
    print(get_data())
