import unittest
from reader_core.rss_classes import RSSItem, RSSNews
import sys

sys.path.append("../")


class TestRssItem(unittest.TestCase):
    def test_RSSItem_create_from_empty_dict(self):
        RSSItem(**{})

    def test_RSSItem_str(self):
        self.assertEqual("Title: \nDate: \nLink: ", str(RSSItem(**{})))

    def test_RSSItem_as_dict(self):
        self.assertEqual({'Title': '', 'Date': '', 'Link': ''}, RSSItem(**{}).as_dict())


class TestRssNews(unittest.TestCase):
    def test_RSSNews_create_from_empty_dict(self):
        RSSNews(**{})

    def test_RSSNews_str(self):
        print(str(RSSNews(**{})))
        self.assertEqual("\n [link: ]\n\n\nSorry, no news for you...", str(RSSNews(**{})))
