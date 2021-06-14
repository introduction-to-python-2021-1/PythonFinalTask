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

    def test_strip_text(self):
        """
        Test replacing wrong character
        """
        self.assertEqual("ab'c&", XmlParser(SiteReader()).strip_tag_text("<![CDATA[ab&#039;c&amp;]]>"))
