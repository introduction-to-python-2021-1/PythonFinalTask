import argparse
import datetime
import json
import os
import unittest

import bs4
from bs4 import BeautifulSoup

from rss_reader.reader_app import rss_reader as rrm


class TestRssReader(unittest.TestCase):

    def setUp(self):
        self.args_sample_01 = ['https://news.yahoo.com/rss/', '--limit', '1']

        self.cache_path = 'rss_cache_mock.json'
        self.xml_path = 'yahoo_rss_mock.xml'

        if os.path.basename(os.getcwd()) == 'rss_reader':  # a little trick for running pytest -v --cov=reader_app
            self.xml_path = os.path.join('testing', self.xml_path)
            self.cache_path = os.path.join('testing', self.cache_path)
            self.local_storage_path = os.path.join(os.getcwd(), 'local_storage', 'rss_cache.json')
        else:
            self.local_storage_path = os.path.join(os.path.dirname(os.getcwd()), 'local_storage', 'rss_cache.json')

        with open(self.xml_path, 'rb') as f_obj:
            self.soup_obj = BeautifulSoup(f_obj, features='xml')
            self.xml_binary = f_obj.read()

        with open(self.cache_path, 'r') as f_obj:
            self.all_news_dict = json.load(f_obj)

        self.limit_news_items_args_01 = {
            'news_complete': self.all_news_dict,
            'user_limit': 2,
            'filter_by_date': False,
            'user_date': 0,
        }

        self.limit_news_items_args_02 = {
            'news_complete': self.all_news_dict,
            'user_limit': 0,
            'filter_by_date': False,
            'user_date': 0,
        }

        self.limit_news_items_args_03 = {
            'news_complete': self.all_news_dict,
            'user_limit': 99,
            'filter_by_date': False,
            'user_date': 0,
        }

        self.limit_news_items_args_04 = {
            'news_complete': self.all_news_dict,
            'user_limit': 99,
            'filter_by_date': True,
            'user_date': 20210607,
        }

        self.limit_news_items_args_05 = {
            'news_complete': self.all_news_dict,
            'user_limit': 2,
            'filter_by_date': True,
            'user_date': 20210607,
        }

        self.limit_news_items_args_06 = {
            'news_complete': self.all_news_dict,
            'user_limit': 2,
            'filter_by_date': True,
            'user_date': 999,
        }

    def tearDown(self):
        print('.', end='')

    def test_logging_settings(self):
        result_true = rrm.logging_settings(True)
        result_false = rrm.logging_settings(False)
        self.assertEqual(result_true['level'], 20)
        self.assertEqual(result_false['level'], 999)

    def test_run_parser(self):
        result = rrm.run_parser(self.args_sample_01)
        self.assertIsInstance(result, argparse.Namespace)

    def test_get_cache_path(self):
        self.assertEqual(rrm.get_cache_path(os.getcwd()), self.local_storage_path)

    def test_get_soup_object(self):
        result = rrm.get_soup_object(self.xml_binary)
        self.assertIsInstance(result, bs4.BeautifulSoup)

    def test_collect_news_items(self):
        result = rrm.collect_news_items(self.soup_obj)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['Items count'], 50)
        self.assertEqual(result['Feed'], 'Yahoo News - Latest News & Headlines')

    def test_get_user_limit(self):
        self.assertEqual(rrm.get_user_limit(self.all_news_dict, 0), 50)
        self.assertEqual(rrm.get_user_limit(self.all_news_dict, 20), 20)
        self.assertEqual(rrm.get_user_limit(self.all_news_dict, 99), 50)

    def test_limit_news_items(self):
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_01)['Items']), 2)
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_02)['Items']), 50)
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_03)['Items']), 50)

        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_04)['Items']), 21)
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_05)['Items']), 2)

    def test_get_date_obj(self):
        self.assertEqual(rrm.get_date_obj(20210608), datetime.date(2021, 6, 8))
        self.assertRaises(ValueError, rrm.get_date_obj, 202106098)

    def test_source_is_valid(self):
        self.assertTrue(rrm.source_is_valid('https://news.yahoo.com/rss/'))
        self.assertFalse(rrm.source_is_valid('abrakadabra'))


if __name__ == "__main__":
    unittest.main()
