import argparse
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from io import StringIO

from rssreader import rss_reader


class TestArgs(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_verbose_arg(self, mock_stdout):
        argparse.ArgumentParser.parse_args = MagicMock(
            return_value=argparse.Namespace(limit=1, verbose=True, source="https://news.yahoo.com/rss/"))
        rss_reader.main()
        self.assertTrue("[INFO]" in mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_negative_limit_arg(self, mock_stdout):
        argparse.ArgumentParser.parse_args = MagicMock(
            return_value=argparse.Namespace(limit=-1, verbose=False, source="https://news.yahoo.com/rss/"))
        rss_reader.main()
        self.assertTrue("[ERROR]" in mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_wrong_limit_arg(self, mock_stdout):
        argparse.ArgumentParser.parse_args = MagicMock(
            return_value=argparse.Namespace(limit="a", verbose=False, source="https://news.yahoo.com/rss/"))
        with self.assertRaises(SystemExit) as cm:
            rss_reader.main()
        self.assertEqual(cm.exception.code, 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_json_arg(self, mock_stdout):
        argparse.ArgumentParser.parse_args = MagicMock(
            return_value=argparse.Namespace(limit=1, verbose=False, source="https://news.yahoo.com/rss/", json=True))
        rss_reader.main()
        self.assertTrue("News\": [" in mock_stdout.getvalue())

