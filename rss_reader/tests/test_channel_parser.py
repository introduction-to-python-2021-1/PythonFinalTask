import unittest
from unittest import mock

import xml.etree.ElementTree as ET

from rss_reader import channel_parse


class TestChannelParser(unittest.TestCase):

    @mock.patch("rss_reader.channel_parse.get_xml_tree", return_value=ET.parse("correct_fake_rss.xml"))
    def test_get_xml_tree_from_correct(self, mock_get_xml_tree):
        root = channel_parse.get_xml_tree("correct_fake_rss.xml")
        self.assertEqual("Yahoo News - Latest News & Headlines", root.findtext("channel/title"))
