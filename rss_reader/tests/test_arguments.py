from io import StringIO
import json
import logging
import os
import re
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from components.feed import Feed
from rss_reader.rss_reader.rss_reader import main


class TestRssReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/example.xml')), 'r') as file:
            cls.soup = BeautifulSoup(file.read(), 'lxml-xml')
        cls.example_feed_title = cls.soup.find('title').text
        cls.example_items = cls.soup.find_all('item')
        cls.example_feed = Feed('https://www.yahoo.com/news', None, False, logging, cls.example_feed_title,
                                cls.example_items)
        cls.example_news_list = cls.example_feed.news_list

    @patch('sys.stdout', new_callable=StringIO)
    def test_version(self, mock_stdout):
        """Tests that if --version option is specified app should just print its version and stop"""
        argv = ['--version']
        with self.assertRaises(SystemExit):
            main(argv)
        self.assertEqual(mock_stdout.getvalue(), 'Version 0.4\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_version_with_the_provided_source(self, mock_stdout):
        """Tests that if source URL and --version option is specified app should just print its version and stop"""
        argv = ['https://news.yahoo.com/rss/', '--version']
        with self.assertRaises(SystemExit):
            main(argv)
        self.assertEqual(mock_stdout.getvalue(), 'Version 0.4\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_limit(self, mock_stdout):
        """Tests that if --limit is specified user should get specified number of news"""
        with patch.object(self.example_feed, 'news_limit', 2):
            print(str(self.example_feed))
        result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', mock_stdout.getvalue())
        self.assertEqual(len(result_news_dates_and_links), 2)

    @patch('sys.stdout', new_callable=StringIO)
    def test_limit_larger_than_feed_size(self, mock_stdout):
        """Tests that if --limit is larger than feed size then user should get all available news"""
        with patch.object(self.example_feed, 'news_limit', 999):
            print(str(self.example_feed))
        result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', mock_stdout.getvalue())
        self.assertEqual(len(result_news_dates_and_links), 5)

    @patch('sys.stdout', new_callable=StringIO)
    def test_limit_is_not_specified(self, mock_stdout):
        """Tests that if --limit is not specified, then user should get all available feed"""
        with patch.object(self.example_feed, 'news_limit', None):
            print(str(self.example_feed))
        result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', mock_stdout.getvalue())
        self.assertEqual(len(result_news_dates_and_links), 5)

    @patch('sys.stdout', new_callable=StringIO)
    def test_json(self, mock_stdout):
        """Tests that if --json option is specified utility should convert the news into JSON format"""
        with patch.object(self.example_feed, 'to_json', True):
            print(str(self.example_feed))
        try:
            json.loads(mock_stdout.getvalue())
        except json.JSONDecodeError:
            self.fail('JSONDecodeError raised by json.loads')

    @patch('sys.stdout', new_callable=StringIO)
    def test_json_with_limit(self, mock_stdout):
        """
        Tests that if --limit and --json option is specified utility should convert the news into JSON format
        and user should get specified number of news
        """
        with patch.object(self.example_feed, 'to_json', True):
            with patch.object(self.example_feed, 'news_limit', 2):
                print(str(self.example_feed))
        try:
            result_json = json.loads(mock_stdout.getvalue())
        except json.JSONDecodeError:
            self.fail('JSONDecodeError raised by json.loads')
        else:
            self.assertEqual(len(result_json['0']['items']), 2)


if __name__ == '__main__':
    unittest.main()
