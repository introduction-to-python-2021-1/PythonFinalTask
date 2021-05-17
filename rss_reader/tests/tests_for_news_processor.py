import unittest
import sys
sys.path.append("../")

from reader_core.news_processor import NewsProcessor


class TestNewsProcessor(unittest.TestCase):
    def test_get_news_with_empty_parser(self):
        proc = NewsProcessor(1)
        proc.get_news("https://news.yahoo.com/rss/" )