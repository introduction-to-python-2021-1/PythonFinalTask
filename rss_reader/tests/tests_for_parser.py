"""
    This module covers with tests code of parser.py
"""
import unittest
from unittest.mock import MagicMock
from rss_core.parser import XmlParser
from rss_core.reader import SiteReader

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
</rss>""".replace("\n", "").replace("\t", "")

print(XML_INFO)

CORRECT_NEWS_DICT = {}


class TestParser(unittest.TestCase):
    """
    Test XmlParser
    """

    def setUp(self):
        self.get_data = SiteReader.get_data

    def tearDown(self):
        SiteReader.get_data = self.get_data

    def test_empty_reader(self):
        """
        Test work of parser with empty reader

        """
        parser = XmlParser()
        self.assertRaises(AttributeError, parser.parse_news, "http")

    def test_not_empty_parser(self):
        SiteReader.get_data = MagicMock(return_value=XML_INFO.replace("\n", ""))
        parser = XmlParser(SiteReader())
        news_dict = parser.parse_news("http://abc")
        self.assertTrue(isinstance(news_dict, dict))

    def test_get_invalid_xml(self):
        """
        Test parsing news from bad xml or not xml response
        """
        SiteReader.get_data = MagicMock(return_value="<h1><")
        parser = XmlParser(SiteReader())
        with self.assertRaises(SystemExit) as cm:
            parser.parse_news("http")
        self.assertEqual(cm.exception.code, 1)

    def test_strip_text(self):
        """
        Test replacing wrong character
        """
        self.assertEqual("ab'c&", XmlParser(SiteReader()).strip_tag_text("<![CDATA[ab&#039;c&amp;]]>"))
