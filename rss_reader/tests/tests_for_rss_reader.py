"""
    This module covers with tests code of rss_reader.py
"""
import argparse
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from io import StringIO

from rss_core.reader import SiteReader
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

    def setUp(self):
        self.get_args = rss_reader.get_args

    def tearDown(self):
        rss_reader.get_args = self.get_args

    @patch('sys.stdout', new_callable=StringIO)
    def test_verbose_arg(self, mock_stdout):
        """ Test --verbose argument """
        SiteReader.get_data = MagicMock(return_value=XML_INFO)
        rss_reader.get_args = MagicMock(
            return_value=argparse.Namespace(limit=1, verbose=True, json=False, source="https://news.yahoo.com/rss/"))
        rss_reader.main()
        self.assertTrue("[INFO]" in mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_limit_arg(self, mock_stdout):
        """ Tests --limit argument """
        SiteReader.get_data = MagicMock(return_value=XML_INFO)
        rss_reader.get_args = MagicMock(
            return_value=argparse.Namespace(limit=-1, verbose=False, json=False, source="https://news.yahoo.com/rss/"))

        with self.assertRaises(SystemExit) as cm:
            rss_reader.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertTrue("[ERROR] Limit should be positive integer" in mock_stdout.getvalue())

        rss_reader.get_args = MagicMock(
            return_value=argparse.Namespace(limit="a", verbose=False, json=False, source="https://news.yahoo.com/rss/"))
        with self.assertRaises(SystemExit) as cm:
            rss_reader.main()
        self.assertEqual(cm.exception.code, 1)

        rss_reader.get_args = MagicMock(
            return_value=argparse.Namespace(limit=3, verbose=False, json=False, source="https://news.yahoo.com/rss/"))
        rss_reader.main()
        self.assertEqual(2, mock_stdout.getvalue().count("News title"))

    @patch('sys.stdout', new_callable=StringIO)
    def test_version_arg(self, mock_stdout):
        """Test --version"""
        with self.assertRaises(SystemExit) as cm:
            rss_reader.get_args({"--version": True})
        self.assertEqual(cm.exception.code, 0)
        self.assertTrue("Version" in mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_json_arg(self, mock_stdout):
        SiteReader.get_data = MagicMock(return_value=XML_INFO)
        rss_reader.get_args = MagicMock(
            return_value=argparse.Namespace(limit=1, verbose=False, source="https://news.yahoo.com/rss/", json=True))
        rss_reader.main()
        self.assertEqual(RSS_JSON, mock_stdout.getvalue())
