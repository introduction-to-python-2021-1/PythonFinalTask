import unittest
from unittest import mock
import sys
from io import StringIO

import xml.etree.ElementTree as ET

from rss_reader import feed_container
from rss_reader import channel_parse


@mock.patch("rss_reader.channel_parse.get_xml_tree", return_value=ET.parse("correct_fake_rss.xml"))
class TestFeedContainer(unittest.TestCase):

    def test_get_feed_title(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertEqual(feed.feed_title, "Yahoo News - Latest News & Headlines")

    def test_get_feed_link(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertEqual(feed.feed_link, "https://www.yahoo.com/news")

    def test_get_feed_description(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertEqual(feed.feed_description,
                         "The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.")

    def test_get_feed_date(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertEqual(feed.feed_date, "Sun, 06 Jun 2021 11:07:10 -0400")

    def test_get_feed_copyright(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertEqual(feed.feed_copyright, "Copyright (c) 2021 Yahoo! Inc. All rights reserved")

    def test_get_news(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertIsInstance(feed.get_news(), list)

    def test_get_news_large(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertTrue(len(feed.get_news()) == 50)

    def test_get_news_large(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertTrue(len(feed.get_news_to_save()) == 50)

    def test_get_news_by_date(self, mock_get_xml_tree):
        feed = feed_container.FeedContainer("fake_rss.xml")
        self.assertTrue(len(feed.get_news_by_date("20210503")) == 0)
