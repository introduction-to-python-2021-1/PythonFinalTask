import unittest
from unittest.mock import patch
from rss_reader.Rss_reader import RssParser


class FeedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'url'
        self.limit = 2
        self.parser = RssParser(self.url, self.limit)

    def test_url(self):
        self.assertEqual(self.parser.url, self.url)

    def test_count(self):
        self.assertEqual(self.parser.limit, self.limit)

    @patch('rss_reader_files.rss_reader_files.get_img')
    @patch('feedparser.parse')
    def test_feed_parser(self, parse_mock, get_img_mock):
        test_time = (2021, 5, 19, 21, 22, 56, 2, 139, 0)
        parse_mock.return_value = {'bozo': None, 'feed': {'title': 'test_title'},
                                   'entries': [{'title': 'test_title', 'published_parsed': test_time,
                                                'link': 'test_link'}]}
        get_img_mock.return_value = [{'src': 'test_src', 'alt': 'test_alt'}]
        result_feed = self.parser.get_feed()
        parse_mock.assert_called_with(self.parser.url)
        feed_item = result_feed[0]
        self.assertEqual(feed_item.title, 'test_title')
        self.assertEqual(feed_item.link, 'test_link')
        self.assertEqual(feed_item.img[0]['src'], 'test_src')
        self.assertEqual(feed_item.img[0]['alt'], 'test_alt')
        self.assertEqual(feed_item.date, '21-05-19 21:22')

    def test_convert_to_json(self):
        json_news = '{"url": "url", "feed": {"name": "", "items": []}}'
        self.assertEqual(self.parser.convert_to_json(), json_news)


if __name__ == '__main__':
    unittest.main()
