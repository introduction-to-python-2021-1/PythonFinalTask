import unittest
from unittest.mock import MagicMock

from rssreader.rss_core.parser import XMLParser
from rssreader.rss_core.reader import SiteReader


class TestParser(unittest.TestCase):
    def test_empty_reader(self):
        parser = XMLParser()
        self.assertRaises(AttributeError, parser.parse_news, "https://news.yahoo.com/rss/")

    def test_non_rss_url(self):
        parser = XMLParser(SiteReader())
        self.assertEqual({}, parser.parse_news("https://google.com"))

    def test_strip_text(self):
        self.assertEqual("ab'c&", XMLParser(SiteReader()).strip_tag_text("<![CDATA[ab&#039;c&amp;]]>"))


class TestParserParseNews(unittest.TestCase):
    def setUp(self):
        with open('xml_for_test.txt', encoding="utf8") as f:
            xml_content = f.read()
        self.reader = SiteReader()
        self.reader.get_data = MagicMock(return_value=xml_content)

    def tearDown(self):
        self.reader = None

    def test_invalid_limit(self):
        parser = XMLParser(self.reader)
        self.assertRaises(TypeError, parser.parse_news, "https://news.yahoo.com/rss/", 'a')
        self.assertRaises(ValueError, parser.parse_news, "https://news.yahoo.com/rss/", -1)

