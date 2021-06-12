# Author: Julia Los <los.julia.v@gmail.com>.

"""Python command-line RSS reader

Test functions functions for work with local storage of loaded news.
"""

import logging
import os
import unittest

from io import StringIO
from rss_reader.rss_reader.local_storage import convert_date_format, load_from_storage, save_to_storage
from unittest.mock import patch

_test_data_json_filename = r'tests/test_storage.json'
_test_tmp_json_filename = r'tests/test_temp_storage.json'


class LocalStorageTests(unittest.TestCase):
    """Test functions for work with local storage of loaded news."""

    @staticmethod
    def _delete_file(filename):
        """Delete specified file."""
        if os.path.isfile(filename):
            os.remove(filename)

    @staticmethod
    def _init_test_logger(name, stream):
        """Initialization logger object."""
        logger = logging.getLogger(name)
        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger

    def test_convert_date_format_for_None(self):
        """Test convert_date_format() function for None."""
        self.assertEqual(convert_date_format(None, None, None), '')

    def test_convert_date_format_for_incorrect_format(self):
        """Test convert_date_format() function for incorrect string."""
        self.assertEqual(convert_date_format('none', 'none', 'none'), 'none')

    def test_convert_date_format_for_incorrect_string(self):
        """Test convert_date_format() function for incorrect string."""
        self.assertEqual(convert_date_format('none', '%a, %d %b, %Y %I:%M %p', '%Y%m%d'), '')

    def test_convert_date_format_from_long_to_short(self):
        """Test convert_date_format() function from long to short format."""
        self.assertEqual(convert_date_format('Sun, 23 May, 2021 05:30 PM', '%a, %d %b, %Y %I:%M %p', '%Y%m%d'),
                         '20210523')

    def test_convert_date_format_from_short_to_long(self):
        """Test convert_date_format() function from short to long format."""
        self.assertRegex(convert_date_format('20210523', '%Y%m%d', '%a, %d %b, %Y %I:%M %p'),
                         'Sun, 23 May, 2021')

    def test_load_from_storage_for_None_date_argument(self):
        """Test load_from_storage() function for None date argument."""
        self.assertIsNone(load_from_storage('', None))

    def test_load_from_storage_for_empty_storage(self):
        """Test load_from_storage() function for empty storage."""
        self.assertIsNone(load_from_storage('', '20210524'))

    def test_load_from_storage_for_empty_storage_with_logger(self):
        """Test load_from_storage() function for empty storage with logger."""
        with patch('sys.stdout', new=StringIO()) as test_out:
            load_from_storage('', '20210524', logger=self._init_test_logger('test_local_storage', test_out))
            self.assertTrue(test_out.getvalue().find("Local storage does not exist.") != -1)

    def test_load_from_storage_for_full_storage(self):
        """Test load_from_storage() function for full storage."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Mon, 24 May, 2021 10:14 AM',
                      'image': 'http://test.com/image.jpg',
                      'description': 'Last news'},
                 ]}]
        self.assertEqual(load_from_storage(_test_data_json_filename, '20210524'), data)

    def test_save_to_storage_for_None(self):
        """Test save_to_storage() function for None."""
        self._delete_file(_test_tmp_json_filename)
        save_to_storage(_test_tmp_json_filename, None)
        self.assertFalse(os.path.isfile(_test_tmp_json_filename))
        self._delete_file(_test_tmp_json_filename)

    def test_save_to_storage_for_empty_data(self):
        """Test save_to_storage() function for empty data."""
        self._delete_file(_test_tmp_json_filename)
        save_to_storage(_test_tmp_json_filename, {})
        self.assertFalse(os.path.isfile(_test_tmp_json_filename))
        self._delete_file(_test_tmp_json_filename)

    def test_save_to_storage_for_empty_data_with_logger(self):
        """Test save_to_storage() function for empty data with logger."""
        self._delete_file(_test_tmp_json_filename)
        with patch('sys.stdout', new=StringIO()) as test_out:
            save_to_storage(_test_tmp_json_filename, {}, logger=self._init_test_logger('test_local_storage', test_out))
            self.assertTrue(test_out.getvalue().find("Data is empty.") != -1)
        self._delete_file(_test_tmp_json_filename)

    def test_save_to_storage_for_full_data(self):
        """Test save_to_storage() function for full data."""
        self._delete_file(_test_tmp_json_filename)
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Mon, 24 May, 2021 10:14 AM',
                      'image': '',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'image': '',
                      'description': ''},
                 ]}]
        save_to_storage(_test_tmp_json_filename, data)
        self.assertTrue(os.path.exists(_test_tmp_json_filename))
        self._delete_file(_test_tmp_json_filename)


if __name__ == '__main__':
    unittest.main()
