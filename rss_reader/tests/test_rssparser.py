from os.path import join
from unittest import TestCase
from unittest.mock import Mock

from rootpath import detect

from modules.rssparser import RSSparser

news_file = join(detect(), 'rss_reader', 'data', 'example', 'news.xml')
with open(news_file, 'r') as file:
    news = file.read()


class TestRSSparser(TestCase):
    def setUp(self) -> None:
        self.parser = RSSparser(source=news, url='https://www.rt.com/rss/news/', logger=Mock())

    def test_limit_more_news_count(self):
        self.assertEqual(len(self.parser.parse_news(limit=999)), self.parser.news_count)

    def test_negative_limit(self):
        self.assertEqual(len(self.parser.parse_news(limit=-999)), self.parser.news_count)

    def test_zero_limit(self):
        self.assertEqual(len(self.parser.parse_news(limit=0)), self.parser.news_count)

    def test_correct_limit(self):
        self.assertEqual(len(self.parser.parse_news(limit=2)), 2)
