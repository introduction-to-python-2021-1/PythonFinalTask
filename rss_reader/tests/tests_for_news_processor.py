import unittest

from rssreader.rss_core.news_processor import NewsProcessor
from rssreader.rss_core.parser import XMLParser
from rssreader.rss_core.reader import SiteReader


class TestNewsProcessor(unittest.TestCase):
    def test_get_news_with_empty_parser(self):
        proc = NewsProcessor(1)
        proc.get_news("https://news.yahoo.com/rss/")

    def test_get_news_wrong_link(self):
        proc = NewsProcessor(XMLParser(SiteReader()))
        proc.get_news("")
        proc.get_news(1)
