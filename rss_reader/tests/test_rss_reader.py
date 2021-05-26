# Author: Julia Los <los.julia.v@gmail.com>.

"""Test command-line RSS reader."""

import feedparser
import os
import unittest

from io import StringIO
from rss_reader.rss_reader import RSSReader
from time import strptime
from unittest.mock import patch

_test_data_xml_filename = r'tests/test_rss.xml'
_test_data_json_filename = r'tests/test_storage.json'
_test_results_txt_filename = r'tests/test_results.txt'
_test_tmp_json_filename = r'tests/test_temp_storage.json'


class RSSReaderTests(unittest.TestCase):
    """Test functions of RSSReader class."""

    def test_parse_url_for_None(self):
        """Test _parse_url() function for None."""
        self.assertIsNone(RSSReader(source=None)._parse_url())

    def test_parse_url_for_empty_url(self):
        """Test _parse_url() function for empty url."""
        self.assertIsNone(RSSReader(source='')._parse_url())

    def test_parse_url_for_incorrect_url(self):
        """Test _parse_url() function for correct url."""
        self.assertIsNotNone(RSSReader(source='https://www.wikipedia.org/')._parse_url())

    def test_parse_url_for_correct_url(self):
        """Test _parse_url() function for correct url."""
        self.assertIsNotNone(RSSReader(source='https://news.yahoo.com/rss/')._parse_url())

    def test_convert_date_format_for_None(self):
        """Test _convert_date_format() function for None."""
        self.assertEqual(RSSReader()._convert_date_format(None, None, None), '')

    def test_convert_date_format_for_incorrect_format(self):
        """Test _convert_date_format() function for incorrect string."""
        self.assertEqual(RSSReader()._convert_date_format('none', 'none', 'none'), 'none')

    def test_convert_date_format_for_incorrect_string(self):
        """Test _convert_date_format() function for incorrect string."""
        self.assertEqual(RSSReader()._convert_date_format('none', '%a, %d %b, %Y %I:%M %p', '%Y%m%d'), '')

    def test_convert_date_format_from_long_to_short(self):
        """Test _convert_date_format() function from long to short format."""
        self.assertEqual(RSSReader()._convert_date_format('Sun, 23 May, 2021 05:30 PM',
                                                          '%a, %d %b, %Y %I:%M %p', '%Y%m%d'), '20210523')

    def test_convert_date_format_from_short_to_long(self):
        """Test _convert_date_format() function from short to long format."""
        self.assertRegex(RSSReader()._convert_date_format('20210523', '%Y%m%d', '%a, %d %b, %Y %I:%M %p'),
                         'Sun, 23 May, 2021')

    def test_load_from_storage_for_None_date_argument(self):
        """Test _load_from_storage() function for None date argument."""
        self.assertIsNone(RSSReader()._load_from_storage(''))

    def test_load_from_storage_for_empty_storage(self):
        """Test _load_from_storage() function for empty storage."""
        self.assertIsNone(RSSReader(date='20210524')._load_from_storage(''))

    def test_load_from_storage_for_full_storage(self):
        """Test _load_from_storage() function for full storage."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Mon, 24 May, 2021 10:14 AM',
                      'description': 'Last news'},
                 ]}]
        self.assertEqual(RSSReader(date='20210524')._load_from_storage(_test_data_json_filename), data)

    @staticmethod
    def _test_delete_file(filename):
        """Delete specified file."""
        if os.path.isfile(filename):
            os.remove(filename)

    def test_save_to_storage_for_None(self):
        """Test _save_to_storage() function for None."""
        self._test_delete_file(_test_tmp_json_filename)
        RSSReader()._save_to_storage(_test_tmp_json_filename, None)
        self.assertFalse(os.path.isfile(_test_tmp_json_filename))
        self._test_delete_file(_test_tmp_json_filename)

    def test_save_to_storage_for_empty_data(self):
        """Test _save_to_storage() function for empty data."""
        self._test_delete_file(_test_tmp_json_filename)
        RSSReader()._save_to_storage(_test_tmp_json_filename, {})
        self.assertFalse(os.path.isfile(_test_tmp_json_filename))
        self._test_delete_file(_test_tmp_json_filename)

    def test_save_to_storage_for_full_data(self):
        """Test _save_to_storage() function for full data."""
        self._test_delete_file(_test_tmp_json_filename)
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Mon, 24 May, 2021 10:14 AM',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'description': ''},
                 ]}]
        RSSReader()._save_to_storage(_test_tmp_json_filename, data)
        self.assertTrue(os.path.exists(_test_tmp_json_filename))
        self._test_delete_file(_test_tmp_json_filename)

    def test_format_date_for_None(self):
        """Test _format_date() function for None."""
        self.assertEqual(RSSReader()._format_date(None, '%a, %d %b, %Y %I:%M %p'), '')

    def test_format_date_for_int(self):
        """Test _format_date() function for int."""
        self.assertEqual(RSSReader()._format_date(5, '%a, %d %b, %Y %I:%M %p'), '')

    def test_format_date_for_incorrect_string(self):
        """Test _format_date() function for incorrect string."""
        self.assertEqual(RSSReader()._format_date("Error date", '%a, %d %b, %Y %I:%M %p'), '')

    def test_format_date_for_correct_string(self):
        """Test _format_date() function for correct string."""
        self.assertEqual(RSSReader()._format_date(strptime('Sun, 23 May, 2021 05:30 PM', '%a, %d %b, %Y %I:%M %p'),
                                                  '%a, %d %b, %Y %I:%M %p'), 'Sun, 23 May, 2021 05:30 PM')

    def test_load_data_for_None(self):
        """Test _load_date() function for None."""
        self.assertIsNone(RSSReader()._load_data(None))

    def test_load_data_for_empty_channel(self):
        """Test _load_date() function for empty channel."""
        parser = feedparser.parse('')
        self.assertIsNone(RSSReader()._load_data(parser))

    def test_load_data_for_full_data(self):
        """Test _load_date() function for full data."""
        parser = feedparser.parse(_test_data_xml_filename)
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Mon, 24 May, 2021 10:14 AM',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'description': ''},
                 ]}]
        self.assertEqual(RSSReader()._load_data(parser), data)

    @staticmethod
    def _test_result(filename, beg_line, end_line):
        """Read data from file."""
        with open(filename, 'r', encoding="utf-8") as f:
            result = f.readlines()
        return "".join(result[beg_line:end_line + 1])

    def _test_print(self, func, data, expected):
        """Write data to fake output."""
        with patch('sys.stdout', new=StringIO()) as test_out:
            func(data)
            self.assertEqual(test_out.getvalue(), expected)

    def test_print_as_formatted_text_for_None(self):
        """Test _print_as_formatted_text() function for None."""
        self._test_print(RSSReader()._print_as_formatted_text, None, '')

    def test_print_as_formatted_text_for_empty_data(self):
        """Test _print_as_formatted_text() function for empty data."""
        self._test_print(RSSReader()._print_as_formatted_text, {}, '')

    def test_print_as_formatted_text_for_only_channel(self):
        """Test _print_as_formatted_text() function for only channel."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel'}]
        expected = self._test_result(_test_results_txt_filename, 1, 2)
        self._test_print(RSSReader()._print_as_formatted_text, data, expected)

    def test_print_as_formatted_text_for_full_data(self):
        """Test _print_as_formatted_text() function for full data."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Sun, 23 May, 2021 05:30 PM',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'description': ''},
                 ]}]
        expected = self._test_result(_test_results_txt_filename, 5, 18)
        self._test_print(RSSReader()._print_as_formatted_text, data, expected)

    def test_print_as_json_for_None(self):
        """Test _print_as_json() function for None."""
        self._test_print(RSSReader()._print_as_json, None, '')

    def test_print_as_json_for_empty_data(self):
        """Test _print_as_json() function for empty data."""
        self._test_print(RSSReader()._print_as_json, {}, '')

    def test_print_as_json_for_only_channel(self):
        """Test _print_as_json() function for only channel."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel'}]
        expected = self._test_result(_test_results_txt_filename, 21, 26)
        self._test_print(RSSReader()._print_as_json, data, expected)

    def test_print_as_json_for_full_data(self):
        """Test _print_as_json() function for full data."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Sun, 23 May, 2021 05:30 PM',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'description': ''},
                 ]}]
        expected = self._test_result(_test_results_txt_filename, 29, 52)
        self._test_print(RSSReader()._print_as_json, data, expected)


if __name__ == '__main__':
    unittest.main()
