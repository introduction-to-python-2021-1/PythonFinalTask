import unittest

from rss_core.parser import XMLParser
from rss_core.reader import SiteReader


class TestParser(unittest.TestCase):
    def test_empty_reader(self):
        parser = XMLParser()
        self.assertRaises(AttributeError, parser.parse_news, "https://news.yahoo.com/rss/")

    def test_not_rss_url(self):
        parser = XMLParser(SiteReader())
        self.assertEqual({}, parser.parse_news("https://google.com"))

    def test_strip_text(self):
        self.assertEqual("ab'c&", XMLParser(SiteReader()).strip_tag_text("<![CDATA[ab&#039;c&amp;]]>"))


class TestParserParseNews(unittest.TestCase):

    def test_invalid_limit(self):
        parser = XMLParser(SiteReader())
        self.assertRaises(TypeError, parser.parse_news, "https://news.yahoo.com/rss/", 'a')
        self.assertRaises(ValueError, parser.parse_news, "https://news.yahoo.com/rss/", -1)
