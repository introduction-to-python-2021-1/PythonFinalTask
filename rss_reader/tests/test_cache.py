import filecmp
import json
import logging
import os
import shutil
import unittest

from bs4 import BeautifulSoup

from components.cache import Cache
from components.feed import Feed


class TestRssReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')) + os.path.sep
        cls.cache_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache')) + os.path.sep
        with open(cls.data_folder + 'example.xml', 'r') as file:
            cls.soup = BeautifulSoup(file.read(), 'lxml-xml')
        cls.example_feed_title = cls.soup.find('title').text
        cls.example_items = cls.soup.find_all('item')
        cls.example_feed = Feed('https://www.yahoo.com/news', None, False, logging, cls.example_feed_title,
                                Cache(logging, cls.cache_folder), news_items=cls.example_items)
        cls.example_news_list = cls.example_feed.news_list
        shutil.rmtree(cls.cache_folder)

    def setUp(self):
        self.cache = Cache(logging, self.cache_folder)

    def tearDown(self):
        shutil.rmtree(self.cache_folder)

    def test_cache_news(self):
        """Tests that news is cached to a file"""
        self.cache.cache_news(self.example_news_list[0])
        self.assertTrue(
            filecmp.cmp(self.data_folder + 'cached_news.json', self.cache_folder + '20210505.json'))

    def test_get_news_from_cache(self):
        """Tests that news are correctly fetched from the cache"""
        self.cache.cache_news(self.example_news_list[0])
        feeds_list = self.cache.get_news_from_cache('20210505', None, None, False)
        self.assertEqual(feeds_list[0].news_list[0].to_dict(), self.example_news_list[0].to_dict())

    def test_get_news_from_cache_with_limit(self):
        """Tests that the --limit argument affects the news feed fetched from the cache"""
        for example_news in self.example_news_list:
            self.cache.cache_news(example_news)
        feeds_list = self.cache.get_news_from_cache('20210505', None, 2, False)
        self.assertEqual(len(feeds_list[0].news_list), 2)

    def test_get_news_from_cache_with_json(self):
        """Tests that the --json argument affects the news feed fetched from the cache"""
        for example_news in self.example_news_list:
            self.cache.cache_news(example_news)
        feeds_list = self.cache.get_news_from_cache('20210505', None, None, True)
        try:
            json.loads(str(feeds_list[0]))
        except json.JSONDecodeError:
            self.fail('JSONDecodeError raised by json.loads')

    def test_get_news_from_cache_with_json_and_limit(self):
        """Tests that the --json and --limit argument affects the news feed fetched from the cache"""
        for example_news in self.example_news_list:
            self.cache.cache_news(example_news)
        feeds_list = self.cache.get_news_from_cache('20210505', None, 2, True)
        try:
            result_json = json.loads(str(feeds_list[0]))
        except json.JSONDecodeError:
            self.fail('JSONDecodeError raised by json.loads')
        else:
            self.assertEqual(len(result_json['0']['items']), 2)
