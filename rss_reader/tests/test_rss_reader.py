# Author: Julia Los <los.julia.v@gmail.com>.

"""Test command-line RSS reader."""

import feedparser
import unittest

from io import StringIO
from rss_reader.rss_reader import RSSReader
from time import strptime
from unittest.mock import patch


class RSSReaderTests(unittest.TestCase):
    """Test functions of RSSReader class."""

    def test_parse_url(self):
        """Test _parse_url() function."""
        self.assertIsNone(RSSReader(source=None)._parse_url())
        self.assertIsNone(RSSReader(source='')._parse_url())
        self.assertIsNotNone(RSSReader(source='www.wikipedia.org/')._parse_url())
        self.assertIsNotNone(RSSReader(source='https://news.yahoo.com/rss/')._parse_url())

    def test_format_date(self):
        """Test _format_date() function."""
        self.assertEqual(RSSReader()._format_date(None), '')
        self.assertEqual(RSSReader()._format_date(strptime('Sun, 23 May, 2021 05:30 PM', '%a, %d %b, %Y %I:%M %p')),
                         'Sun, 23 May, 2021 05:30 PM')
        self.assertEqual(RSSReader()._format_date(5), '')
        self.assertEqual(RSSReader()._format_date("Error date"), '')

    def test_load_data(self):
        """Test _load_date() function."""
        # None
        self.assertIsNone(RSSReader()._load_data(None))
        # Empty channel
        parser = feedparser.parse('')
        self.assertIsNone(RSSReader()._load_data(parser))
        # Full data
        parser = feedparser.parse(r'tests/test_rss.xml')
        data = {'channel': 'News channel',
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
                ]}
        self.assertEqual(RSSReader()._load_data(parser), data)

    @staticmethod
    def _test_result(filename, beg_line, end_line):
        with open(filename, 'r', encoding="utf-8") as f:
            result = f.readlines()
        return "".join(result[beg_line:end_line + 1])

    def _test_print(self, func, data, expected):
        with patch('sys.stdout', new=StringIO()) as test_out:
            func(data)
            self.assertEqual(test_out.getvalue(), expected)

    def test_print_as_formatted_text(self):
        """Test _print_as_formatted_text() function."""
        func = RSSReader()._print_as_formatted_text
        # None
        data = None
        expected = ''
        self._test_print(func, data, expected)
        # Empty data
        data = {}
        expected = ''
        self._test_print(func, data, expected)
        # Only channel
        data = {'channel': 'News channel'}
        expected = self._test_result(r'tests/test_results.txt', 1, 2)
        self._test_print(func, data, expected)
        # Full data
        data = {'channel': 'News channel',
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
                ]}
        expected = self._test_result(r'tests/test_results.txt', 5, 18)
        self._test_print(func, data, expected)

    def test_print_as_json(self):
        """Test _print_as_json() function."""
        func = RSSReader()._print_as_json
        # None
        data = None
        expected = ''
        self._test_print(func, data, expected)
        # Empty data
        data = {}
        expected = ''
        self._test_print(func, data, expected)
        # Only channel
        data = {'channel': 'News channel'}
        expected = self._test_result(r'tests/test_results.txt', 21, 23)
        self._test_print(func, data, expected)
        # Full data
        data = {'channel': 'News channel',
                'news': [
                    {'number': 1,
                     'title': 'Last news',
                     'link': 'https://news.ru/last_news.html',
                     'author': 'Alexey Morozov',
                     'date': 'Sun, 23 May, 2021 05:30 PM',
                     'description': 'Last news'},
                ]}
        expected = self._test_result(r'tests/test_results.txt', 26, 38)
        self._test_print(func, data, expected)


if __name__ == '__main__':
    unittest.main()
