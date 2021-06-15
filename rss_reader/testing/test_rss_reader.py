import argparse
from io import StringIO
import json
import os
import unittest
from unittest.mock import patch

import bs4
from bs4 import BeautifulSoup
from reader_app import rss_reader as rrm


class TestRssReader(unittest.TestCase):

    def setUp(self):
        # determine CWD depending on where tests are launched from: 'rss_reader' or 'testing' folder
        if os.path.basename(os.getcwd()) == 'rss_reader':
            self.prefix_testing = 'testing'
            self.real_cwd = os.path.join(os.getcwd(), self.prefix_testing)
        else:
            self.prefix_testing = None
            self.real_cwd = os.getcwd()

        # define paths to test files
        self.xml_path = os.path.join(self.prefix_testing, 'yahoo_rss_mock.xml')
        self.cache_path = os.path.join(self.prefix_testing, 'rss_cache_mock.json')
        self.local_storage_path = os.path.join(self.prefix_testing, 'local_storage', 'rss_cache.json')

        self.args_sample_01 = ['https://news.yahoo.com/rss/', '--limit', '1']
        self.args_sample_02 = ['https://news.yahoo.com/rss/', '--to-pdf', 'my_rss.pdf', '--to-html', 'my_rss.html']
        self.args_sample_03 = ['--date', '20210614', '--to-pdf', 'my_rss.pdf', '--to-html', 'my_rss.html']
        self.args_sample_04 = ['rss_reader.py', '--date', '20210614', '--limit', '1']
        self.args_sample_05 = ['rss_reader.py', '--date', '9999', '--limit', '99']
        self.args_sample_06 = ['rss_reader.py']
        self.args_sample_07 = ['rss_reader.py', 'https://news.yahoo.com/rss/', '--limit', '-3']

        with open(self.xml_path, 'rb') as f_obj:
            self.xml_binary_1 = f_obj.read().decode()[39:]
            self.xml_binary_2 = f_obj.read().decode()
            self.soup_obj = BeautifulSoup(self.xml_binary_1, features='xml')
        with open(self.cache_path, 'r') as f_obj:
            self.all_news_dict = json.load(f_obj)

        self.limit_news_items_args_01 = {'news_complete': self.all_news_dict, 'user_limit': 2,
                                         'filter_by_date': False, 'user_date': 0, }
        self.limit_news_items_args_02 = {'news_complete': self.all_news_dict, 'user_limit': 0,
                                         'filter_by_date': False, 'user_date': 0, }
        self.limit_news_items_args_03 = {'news_complete': self.all_news_dict, 'user_limit': 99,
                                         'filter_by_date': False, 'user_date': 0, }
        self.limit_news_items_args_04 = {'news_complete': self.all_news_dict, 'user_limit': 99,
                                         'filter_by_date': True, 'user_date': 20210614, }
        self.limit_news_items_args_05 = {'news_complete': self.all_news_dict, 'user_limit': 2,
                                         'filter_by_date': True, 'user_date': 20210607, }
        self.limit_news_items_args_06 = {'news_complete': self.all_news_dict, 'user_limit': 2,
                                         'filter_by_date': True, 'user_date': 999, }
        self.limit_news_items_args_07 = {'news_complete': self.all_news_dict, 'user_limit': 3,
                                         'filter_by_date': True, 'user_date': 20210614, }

    def test_logging_settings(self):
        self.assertEqual(rrm.logging_settings(True)['level'], 20)
        self.assertEqual(rrm.logging_settings(False)['level'], 999)

    def test_run_parser(self):
        result = rrm.run_parser(self.args_sample_01)
        self.assertIsInstance(result, argparse.Namespace)

    def test_get_user_limit(self):
        self.assertEqual(rrm.get_user_limit(self.all_news_dict, 0), 50)
        self.assertEqual(rrm.get_user_limit(self.all_news_dict, 20), 20)
        self.assertEqual(rrm.get_user_limit(self.all_news_dict, 99), 50)

    def test_get_soup_object(self):
        self.assertIsInstance(rrm.get_soup_object(self.xml_binary_1), bs4.BeautifulSoup)
        self.assertRaises(SystemExit, rrm.get_soup_object, self.xml_binary_2)

    def test_limit_news_items(self):
        # no date
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_01)['Items']), 2)
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_02)['Items']), 50)
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_03)['Items']), 50)
        # use date
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_04)['Items']), 15)  # 15 for 14/07
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_05)['Items']), 0)  # 0 for 06/07
        # ValueError & exit because of bad date format
        self.assertRaises(SystemExit, rrm.limit_news_items, **self.limit_news_items_args_06)
        # hit 'break' statement
        self.assertEqual(len(rrm.limit_news_items(**self.limit_news_items_args_07)['Items']), 3)

    def test_source_is_valid(self):
        self.assertTrue(rrm.source_is_valid('https://news.yahoo.com/rss/'))
        self.assertFalse(rrm.source_is_valid('abrakadabra'))

    def test_get_conversion_paths(self):
        self.assertEqual(rrm.get_conversion_paths(self.args_sample_01), ('', ''))
        self.assertEqual(rrm.get_conversion_paths(self.args_sample_02), ('my_rss.pdf', 'my_rss.html'))

    def test_print_news_in_terminal(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            rrm.print_news_in_terminal(self.all_news_dict, False)
            self.assertIn('Printing news in text mode', fake_out.getvalue())
        with patch('sys.stdout', new=StringIO()) as fake_out:
            rrm.print_news_in_terminal(self.all_news_dict, True)
            self.assertIn('Printing news in JSON mode', fake_out.getvalue())

    def test_main(self):
        with self.assertLogs() as captured:
            with patch('sys.argv', self.args_sample_04):
                rrm.main()
                self.assertEqual('Starting program.', captured.records[0].getMessage())
                self.assertEqual('Closing program.', captured.records[-1].getMessage())

        with patch('sys.argv', self.args_sample_05):
            self.assertRaises(SystemExit, rrm.main)

        with patch('sys.argv', self.args_sample_06):
            self.assertRaises(SystemExit, rrm.main)

        with patch('sys.argv', self.args_sample_07):
            self.assertRaises(SystemExit, rrm.main)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
