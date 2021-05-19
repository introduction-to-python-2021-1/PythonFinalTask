import unittest

from rssreader.rss_core.reader import SiteReader


class TestReader(unittest.TestCase):
    def test_get_data_empty_link(self):
        reader = SiteReader()
        reader.get_data("")

    def test_get_data_invalid_link(self):
        reader = SiteReader()
        reader.get_data("https://news.yahoo.com/rs")
