"""
    This module covers with tests code of parser.py
"""
import unittest
from unittest.mock import MagicMock
from rss_core.parser import XmlParser
from rss_core.reader import SiteReader
from tests.tests_data import XML_INFO

CORRECT_NEWS_DICT = {}


class TestParser(unittest.TestCase):
    """
    Test XmlParser
    """

    def test_not_empty_parser(self):
        """
        Test correct work parse_news method with correct xml info
        """
        SiteReader.get_data = MagicMock(return_value=XML_INFO.replace("\n", ""))
        parser = XmlParser(SiteReader())
        news_dict = parser.parse_news("http://abc")
        self.assertEqual("Chanel title", news_dict["title"])

    def test_strip_text(self):
        """
        Test replacing wrong character
        """
        self.assertEqual("ab'c&", XmlParser(SiteReader()).strip_tag_text("<![CDATA[ab&#039;c&amp;]]>"))
