import ddt
import unittest

from rss_reader.local_storage import LocalStorage


@ddt.ddt
class TestSetNewsItemsByUrl(unittest.TestCase):
    """Tests set_news_items_by_url method of LocalStorage object with various arguments."""

    @classmethod
    def setUpClass(cls):
        cls.local_storage = LocalStorage("teststorage")

    def setUp(self):
        """Remembers initial local storage content."""
        self.initial_storage_content = self.local_storage.read_from_storage_file()

    @ddt.file_data("../project_data/json/test_set_news_items_by_url.json")
    def test_set_news_items_by_url(self, url, news_items, expected):
        """Tests set_news_items_by_url method of LocalStorage object with various arguments."""
        self.local_storage.set_news_items_by_url(url, news_items)
        storage_content = self.local_storage.read_from_storage_file()

        self.assertEqual(len(storage_content[url]), expected, "Wrong number")

    def tearDown(self):
        """Returns to local storage its initial content."""
        self.local_storage.write_to_storage_file(self.initial_storage_content)


@ddt.ddt
class TestGetNewsItemsByUrlAndDate(unittest.TestCase):
    """Tests get_news_items_by_url_and_date method of LocalStorage object with various arguments."""

    @classmethod
    def setUpClass(cls):
        cls.local_storage = LocalStorage("teststorage")

    @ddt.file_data("../project_data/json/test_get_news_items_by_url_and_date.json")
    def test_get_news_items_by_url_and_date(self, url, pub_date, expected):
        """Tests get_news_items_by_url_and_date method of LocalStorage object with various arguments."""
        self.assertEqual(
            len(self.local_storage.get_news_items_by_url_and_date(url, pub_date)),
            expected,
            "Wrong output size"
        )


class TestGetNumbeOfNewsItemsByUrl(unittest.TestCase):
    """Tests get_number_of_news_items_by_url method of LocalStorage."""

    @classmethod
    def setUpClass(cls):
        cls.local_storage = LocalStorage("teststorage")

    def test_get_number_of_news_items_by_url(self):
        """Tests get_news_items_by_url_and_date method of LocalStorage object."""
        url = "https://news.yahoo.com/rss/"
        self.assertEqual(self.local_storage.get_number_of_news_items_by_url(url), 2, "Wrong number")


if __name__ == "__main__":
    unittest.main()
