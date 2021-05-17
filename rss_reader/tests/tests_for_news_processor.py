import unittest
import sys
from rss_reader.reader_core.news_processor import NewsProcessor

sys.path.append("../")


class TestNewsProcessor(unittest.TestCase):
    def test_get_news_with_empty_parser(self):
        proc = NewsProcessor(1)
        proc.get_news("https://news.yahoo.com/rss/")
