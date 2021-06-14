"""
    This module covers with tests code of rss_reader.py
"""
import unittest
from rss_core.rss_classes import RssItem, RssNews

RSS_ITEM_DICT = {"title": "-", "link": "-", "pubDate": "-", "guid": "-", "category": "-", "content": ["-"],
                 "description": "-"}
RSS_ITEM_STR = "Title: -\nDate: -\nLink: -\nCategory: -\nDescription: -\nMedia: ['-']"


class TestRssItem(unittest.TestCase):
    """
    Test RssItem class
    """

    def test_rss_item_init(self):
        """
        Check if RssItem initializing from dirt in right way +
        checking work of overloaded __str__
        """
        item = RssItem(**RSS_ITEM_DICT)
        self.assertEqual(RSS_ITEM_STR, str(item))

    def test_rss_item_as_dict(self):
        """
        Check as_dict
        """
        self.assertEqual({'Title': '-', 'Date': '-', 'Link': '-', 'Description': '-', 'Category': '-', 'Media': ['-']},
                         RssItem(**RSS_ITEM_DICT).as_dict())


class TestRssNews(unittest.TestCase):
    """
    Testing of RssNews
    """

    def test_rss_news_str(self):
        """
        Test as_str function
        """
        self.assertEqual("\n [link: ]\n\n\nNo news", RssNews(**{}).as_str())

    def test_rss_news_json(self):
        """Check as_json function"""
        self.assertEqual({"Link": "", "Description": "", "Title": "", "News": []}, RssNews(**{}).as_json())
