"""
    This module covers with tests code of rss_reader.py
"""
import argparse
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from io import StringIO

from rss_core.reader import SiteReader
from rss_core.cacher import DbCacher
from rssreader import rss_reader

XML_INFO = """<?xml version="1.0" encoding="UTF-8"?>
            <rss xmlns:media="http://search/">
               <channel>
                  <title>Chanel title</title>
                  <link>Chanel link</link>
                  <description>Chanel description</description>
                  <item>
                     <title>News title</title>
                     <link>News link</link>
                     <pubDate>News date</pubDate>
                     <guid>news id</guid>
                     <media:content url="Media url" />
                  </item>
                  <item>
                     <title>News title</title>
                     <link>News link</link>
                     <pubDate>News date</pubDate>
                     <guid>news id</guid>
                     <media:content url="Media url" />
                  </item>
               </channel>
            </rss>"""

RSS_JSON = """{
    "Link": "Chanel link",
    "Description": "Chanel description",
    "Title": "Chanel title",
    "News": [
        {
            "Title": "News title",
            "Date": "News date",
            "Link": "News link",
            "Media": [
                "Media url"
            ]
        }
    ]
}
"""


class TestRssReader(unittest.TestCase):
    """
    Tests for rss_reader.py
    """
    SiteReader.get_data = MagicMock(return_value=XML_INFO)
    DbCacher.cache_rss_news = MagicMock(return_value=True)

    @patch('sys.stdout', new_callable=StringIO)
    def test_verbose_arg(self, mock_stdout):
        """
        Test --verbose argument
        """
        rss_reader.main(["--limit", "1", "--verbose", "https://news.yahoo.com/rss/"])
        self.assertIn("[INFO]", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_negative_limit_arg(self, mock_stdout):
        """
        Tests negative --limit argument
        """
        with self.assertRaises(SystemExit) as cm:
            rss_reader.main(["--limit", "-1", "https://news.yahoo.com/rss/"])
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("[ERROR] Limit should be positive integer", mock_stdout.getvalue())

    def test_invalid_str_limit_arg(self):
        """
        Tests invalid str --limit argument
        """
        with self.assertRaises(SystemExit) as cm:
            rss_reader.main(["--limit", "a", "https://news.yahoo.com/rss/"])
        self.assertEqual(cm.exception.code, 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_over_news_count_limit_arg(self, mock_stdout):
        """
        Tests --limit argument which greater than news count
        """
        rss_reader.main(["--limit", "3", "https://news.yahoo.com/rss/"])
        self.assertEqual(2, mock_stdout.getvalue().count("News title"))

    @patch('sys.stdout', new_callable=StringIO)
    def test_version_arg(self, mock_stdout):
        """
        Test --version argument
        """
        with self.assertRaises(SystemExit) as cm:
            rss_reader.main(["--version"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("Version 1.3", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_json_arg(self, mock_stdout):
        """
        Test --json argument
        """
        rss_reader.main(["--limit", "1", "--json", "https://news.yahoo.com/rss/"])
        self.assertEqual(RSS_JSON, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_getting_cache_with_wrong_date(self, mock_stdout):
        """
        Test for getting from cache with wrong date
        """
        with self.assertRaises(SystemExit) as cm:
            rss_reader.main(["--limit", "1", "https://news.yahoo.com/rss/", "--date", "2020"])
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Can't parse date '2020'. Check if it is %Y%m%d format", mock_stdout.getvalue())
