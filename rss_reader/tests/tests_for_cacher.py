"""
    This module covers with tests code of news_processor.py
"""
import os
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

from rss_core.cacher import DbCacher
from rss_core.rss_classes import RssNews

DB_NAME = "testdb.db"


class TestCacher(unittest.TestCase):
    """
    Test DbCacher
    """

    @patch('sys.stdout', new_callable=StringIO)
    def test_load_from_cache(self, mock_stdout):
        """
        Test load_from_cache function
        """
        cache = DbCacher()
        cache._get_channels_info_from_db = MagicMock(return_value=[])
        cache.load_from_cache(rss_link="http://a", date="20210613", show_logs=True)
        self.assertIn("News was restored from cache", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_cache_rss_news(self, mock_stdout):
        """
        Test cache_rss_news function
        """
        cache = DbCacher()
        cache._create_channel_cache = MagicMock(return_value=-1)
        cache._create_news_cache = MagicMock(return_value=None)
        cache.cache_rss_news(rss_news=None, rss_link="", show_logs=True)
        self.assertIn("Nes was cached successfully", mock_stdout.getvalue())
