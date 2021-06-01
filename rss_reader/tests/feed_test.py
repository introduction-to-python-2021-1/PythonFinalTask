"""
Module for testing RssParser class, json converter
"""


import unittest
from unittest.mock import patch
from rss_reader.RssParser import RssParser, convert_to_json
from collections import namedtuple


class FeedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'url'
        self.limit = 2
        self.parser = RssParser(self.url, self.limit)

    def test_url(self):
        """
        Tests if url parses correctly
        """
        self.assertEqual(self.parser.url, self.url)

    def test_limit(self):
        """
        Tests if limit parses correctly
        """
        self.assertEqual(self.parser.limit, self.limit)

    def test_empty_items(self):
        """
        Tests condition of feed absence
        """
        self.assertEqual(self.parser.items, [])

    @patch('rss_reader.RssParser.get_img_container')
    @patch('feedparser.parse')
    def test_feed_parser(self, parse_mock, get_img_mock):
        """
        Tests if RssParser creates correct list with feed items
        """
        test_time = (2021, 5, 19, 21, 22, 56, 2, 139, 0)
        links_list = [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://www'}]
        parse_mock.return_value = {'bozo': None, 'feed': {'title': 'test_title'},
                                   'entries': [{'title': 'test_title', 'published_parsed': test_time,
                                                'link': 'test_link', 'summary': 'some text', 'links': links_list}]}
        get_img_mock.return_value = [{'src': 'test_src', 'alt': 'test_alt'}]
        result_feed = self.parser.get_feed()
        parse_mock.assert_called_with(self.parser.url)
        feed_item = result_feed[0]
        self.assertEqual(feed_item.title, 'test_title')
        self.assertEqual(feed_item.link, 'test_link')
        self.assertEqual(feed_item.content, ['some text'])
        self.assertEqual(feed_item.links, ['https://www'])
        self.assertEqual(feed_item.img[0]['src'], 'test_src')
        self.assertEqual(feed_item.img[0]['alt'], 'test_alt')
        self.assertEqual(feed_item.date, test_time)

    def test_convert_to_json(self):
        """
        Tests that feed is correctly converts in json format
        """
        name = 'test_name'
        title = 'test_title'
        link = 'test_link'
        date = 'test_date'
        img = 'test_img'
        summary_list = 'test_content'
        links = 'test_links'
        fields = 'name, title, link, date, img, content, links'
        item = namedtuple('item', fields)._make((name, title, link, date, img, summary_list, links))
        json_news = ('{"items": ['
                     '{"name": "test_name", '
                     '"title": "test_title", '
                     '"link": "test_link", '
                     '"date": "test_date", '
                     '"img": "test_img", '
                     '"content": "test_content", '
                     '"links": "test_links"}]}')

        self.assertEqual(convert_to_json([item]), json_news)


if __name__ == '__main__':
    unittest.main()
