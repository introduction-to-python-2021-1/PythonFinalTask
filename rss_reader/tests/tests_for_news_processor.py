"""
    This module covers with tests code of news_processor.py
"""
import unittest
from io import StringIO
from unittest.mock import patch

from rss_core.news_processor import NewsProcessor
from rss_core.parser import XMLParser
from rss_core.reader import SiteReader


class TestNewsProcessor(unittest.TestCase):
    """ Test NewsProcessor"""
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_news_wrong_link(self, mock_stdout):
        """ Parse news from empty link"""
        proc = NewsProcessor(XMLParser(SiteReader()))
        with self.assertRaises(SystemExit) as cm:
            proc.get_news("")
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual("[ERROR] Link mast be not empty str", mock_stdout.getvalue().strip())
