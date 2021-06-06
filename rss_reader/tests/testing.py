"""This module contains a base class for tests"""

import logging
import os
import shutil
import unittest

from bs4 import BeautifulSoup

from components.cache import Cache
from components.converter import Converter
from components.feed import Feed


class BaseTest(unittest.TestCase):
    """Base class for tests"""

    @classmethod
    def setUpClass(cls):
        """This method initializes variables used in tests"""
        cls.data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')) + os.path.sep
        cls.cache_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache')) + os.path.sep
        with open(cls.data_folder + 'example.xml', 'r') as file:
            cls.document_data = BeautifulSoup(file.read(), 'lxml-xml')
        cls.example_feed_title = cls.document_data.find('title').text
        cls.example_items = cls.document_data.find_all('item')
        cls.example_feed = Feed('https://www.yahoo.com/news', None, False, False, logging, cls.example_feed_title,
                                Cache(logging, cls.cache_folder), news_items=cls.example_items)
        cls.example_news_list = cls.example_feed.news_list
        shutil.rmtree(cls.cache_folder)
        cls.converter = Converter(logging)

    def setUp(self):
        """This method creates a new object of the class Cache for each test"""
        self.cache = Cache(logging, self.cache_folder)

    def tearDown(self):
        """This method clears the cache folder after each test."""
        shutil.rmtree(self.cache_folder)


def mock_response(status, content):
    """Function that simulate the response from requests.get"""
    mock_response = unittest.mock.Mock()
    mock_response.raise_for_status = unittest.mock.Mock()
    mock_response.status_code = status
    mock_response.content = content
    return mock_response
