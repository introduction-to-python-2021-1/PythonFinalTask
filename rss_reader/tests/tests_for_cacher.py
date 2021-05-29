"""
    This module covers with tests code of news_processor.py
"""
import os
import unittest
from rss_core.cacher import DbCacher
from rss_core.rss_classes import RssNews

DB_NAME = "testdb.db"


class TestCacher(unittest.TestCase):
    """
    Test DbCacher
    """

    def tearDown(self):
        os.remove(DB_NAME)

    def test_cache_rss_news(self):
        """
        Test cache_rss_news
        """
        cacher = DbCacher(DB_NAME)
        news = RssNews(**{})
        try:
            cacher.cache_rss_news(news, "http://a")
            cacher.db_processor.close_connection()
        except Exception:
            self.assertTrue(False)
