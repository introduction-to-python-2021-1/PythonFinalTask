import unittest
from unittest import mock

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

    # def test_get_feed_print_news(self, mock_get_xml_tree):
    # 	feed = feed_container.FeedContainer("fake_rss.xml")
    # 	self.assertEqual(feed.print_news(1), "1\n"
    # 										 "Title: Manchin Comes Out against H.R. 1., Says Partisan Voting Legislation\n"
    # 										 "Date: 2021-06-06T13:36:37Z\n"
    # 										 "Link: https://news.yahoo.com/manchin-comes-against-h-r-133637370.html")
