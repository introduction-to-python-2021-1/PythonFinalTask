"""
    This module covers with tests code of parser.py
"""
import unittest
from unittest.mock import MagicMock
from rss_core.parser import XmlParser
from rss_core.reader import SiteReader


class TestParser(unittest.TestCase):
    """Test XmlParser"""

    def test_empty_reader(self):
        """ Test work of parser with empty reader"""
        parser = XmlParser()
        self.assertRaises(AttributeError, parser.parse_news, "http")

    def test_get_invalid_xml(self):
        """Test parsing news from bad xml or not xml response"""
        SiteReader.get_data = MagicMock(return_value="<h1><")
        parser = XmlParser(SiteReader())
        with self.assertRaises(SystemExit) as cm:
            parser.parse_news("http")
        self.assertEqual(cm.exception.code, 1)

    def test_strip_text(self):
        """Test replacing wrong character"""
        self.assertEqual("ab'c&", XmlParser(SiteReader()).strip_tag_text("<![CDATA[ab&#039;c&amp;]]>"))
