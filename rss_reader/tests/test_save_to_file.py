# Author: Julia Los <los.julia.v@gmail.com>.

"""Python command-line RSS reader

Test functions for save the utility's result to file.
"""

import os
import unittest

from io import StringIO
from rss_reader.rss_reader.save_to_file import check_filename, save_to_fb2, save_to_html
from unittest.mock import patch

_test_tmp_fb2_filename = r'tests/test_temp_fb2.fb2'
_test_tmp_html_filename = r'tests/test_temp_html.html'


class SaveToFileTests(unittest.TestCase):
    """Test functions for save the RSS Reader utility's result to file."""

    @staticmethod
    def _delete_file(filename):
        """Delete specified file."""
        if os.path.isfile(filename):
            os.remove(filename)

    def test_check_filename_for_None(self):
        """Test check_filename() function for None."""
        self.assertIsNone(check_filename(None, '.fb2'))

    def test_check_filename_for_empty_name(self):
        """Test check_filename() function for empty name."""
        self.assertIsNone(check_filename('', '.fb2'))

    def test_check_filename_for_folder(self):
        """Test check_filename() function for folder."""
        self.assertIsNone(check_filename('temp/', '.fb2'))

    def test_check_filename_for_incorrect_extention(self):
        """Test check_filename() function for incorrect extention."""
        self.assertIsNone(check_filename('test.txt', '.fb2'))

    def test_check_filename_for_correct_short_name(self):
        """Test check_filename() function for correct short name."""
        self.assertEqual(check_filename('test', '.fb2'), 'test.fb2')

    def test_check_filename_for_correct_full_name(self):
        """Test check_filename() function for correct full name."""
        self.assertEqual(check_filename('C://PythonTest/test.fb2', '.fb2'), 'C://PythonTest/test.fb2')

    def test_save_to_fb2_for_None(self):
        """Test save_to_fb2() function for None."""
        self._delete_file(_test_tmp_fb2_filename)
        save_to_fb2(_test_tmp_fb2_filename, None)
        self.assertFalse(os.path.isfile(_test_tmp_fb2_filename))
        self._delete_file(_test_tmp_fb2_filename)

    def test_save_to_fb2_for_empty_data(self):
        """Test save_to_fb2() function for empty data."""
        self._delete_file(_test_tmp_fb2_filename)
        save_to_fb2(_test_tmp_fb2_filename, {})
        self.assertFalse(os.path.isfile(_test_tmp_fb2_filename))
        self._delete_file(_test_tmp_fb2_filename)

    def test_save_to_fb2_for_only_channel(self):
        """Test save_to_fb2() function for only channel."""
        self._delete_file(_test_tmp_fb2_filename)
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel'}]
        with patch('sys.stdout', new=StringIO()) as test_out:
            save_to_fb2(_test_tmp_fb2_filename, data)
            self.assertTrue(test_out.getvalue().find("Loaded news save to file:") != -1)
        self._delete_file(_test_tmp_fb2_filename)

    def test_save_to_fb2_for_full_data(self):
        """Test save_to_fb2() function for full data."""
        self._delete_file(_test_tmp_fb2_filename)
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Sun, 23 May, 2021 05:30 PM',
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
        save_to_fb2(_test_tmp_fb2_filename, data)
        self.assertTrue(os.path.exists(_test_tmp_fb2_filename))
        self._delete_file(_test_tmp_fb2_filename)

    def test_save_to_html_for_None(self):
        """Test save_to_html() function for None."""
        self._delete_file(_test_tmp_html_filename)
        save_to_html(_test_tmp_html_filename, None)
        self.assertFalse(os.path.isfile(_test_tmp_html_filename))
        self._delete_file(_test_tmp_html_filename)

    def test_save_to_html_for_empty_data(self):
        """Test save_to_html() function for empty data."""
        self._delete_file(_test_tmp_html_filename)
        save_to_html(_test_tmp_html_filename, {})
        self.assertFalse(os.path.isfile(_test_tmp_html_filename))
        self._delete_file(_test_tmp_html_filename)

    def test_save_to_html_for_only_channel(self):
        """Test save_to_html() function for only channel."""
        self._delete_file(_test_tmp_html_filename)
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel'}]
        with patch('sys.stdout', new=StringIO()) as test_out:
            save_to_html(_test_tmp_html_filename, data)
            self.assertTrue(test_out.getvalue().find("Loaded news save to file:") != -1)
        self._delete_file(_test_tmp_fb2_filename)

    def test_save_to_html_for_full_data(self):
        """Test save_to_html() function for full data."""
        self._delete_file(_test_tmp_html_filename)
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Sun, 23 May, 2021 05:30 PM',
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
        save_to_html(_test_tmp_html_filename, data)
        self.assertTrue(os.path.exists(_test_tmp_html_filename))
        self._delete_file(_test_tmp_html_filename)


if __name__ == '__main__':
    unittest.main()
