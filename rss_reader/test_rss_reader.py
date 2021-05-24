import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup
import requests
import rss_reader

class TestRssReader(unittest.TestCase):
    test_args = ['rss_reader.py', 'http://news.yahoo.com/rss/', '--limit', '1', '--verbose', '--json']


    def test_args_input(self):
        with patch('sys.argv', self.test_args):
            user_args = rss_reader.parsed_args()
            self.assertEqual(user_args.source, 'http://news.yahoo.com/rss/')
            self.assertEqual(user_args.limit, 1)
            self.assertEqual(user_args.verbose, True)
            self.assertEqual(user_args.json, True)


    def test_get_soup_object_class(self):
        args_source = self.test_args[1]
        self.assertIsInstance(rss_reader.get_soup_object(args_source), BeautifulSoup)


    def test_collect_news_items(self):
        limit = int(self.test_args[3])
        r = requests.get(self.test_args[1])
        soup = BeautifulSoup(r.content, features='xml')
        dict_output = rss_reader.collect_news_items(soup, limit)
        self.assertEqual(list(dict_output.keys()), ['Feed', 'Items count', 'Items'])


if __name__ == '__main__':
    unittest.main()