import unittest
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.dirname((os.path.dirname(__file__))))
from reader.RssParser import RssParser


class FeedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'url'
        self.limit = 2
        self.parser = RssParser(self.url, self.limit)

    def test_url(self):
        self.assertEqual(self.parser.url, self.url)

    def test_count(self):
        self.assertEqual(self.parser.limit, self.limit)

    def test_limit(self):
        self.assertEqual(self.parser.limit, self.limit)

    def test_empty_items(self):
        self.assertEqual(self.parser.items, [])

    @patch('reader.RssParser.get_img')
    @patch('feedparser.parse')
    def test_feed_parser(self, parse_mock, get_img_mock):
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
        json_news = '{"url": "url", "feed": {"name": "", "items": []}}'
        self.assertEqual(self.parser.convert_to_json(), json_news)



if __name__ == '__main__':
    unittest.main()
