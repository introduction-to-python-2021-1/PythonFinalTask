# Author: Julia Los <los.julia.v@gmail.com>.

"""Test command-line RSS reader."""

import unittest

from io import StringIO
from rss_reader import RSSReader
from time import strptime
from unittest.mock import patch


class RSSReaderTests(unittest.TestCase):
    """Test functions of RSSReader class."""

    def test_format_date(self):
        """Test _format_date() function."""
        self.assertEqual(RSSReader()._format_date(None), '')
        self.assertEqual(RSSReader()._format_date(strptime('Sun, 23 May, 2021 05:30 PM', '%a, %d %b, %Y %I:%M %p')),
                         'Sun, 23 May, 2021 05:30 PM')
        self.assertEqual(RSSReader()._format_date(5), '')
        self.assertEqual(RSSReader()._format_date("Error date"), '')

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
        expected = self._test_result('test_results.txt', 1, 2)
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
        expected = self._test_result('test_results.txt', 5, 18)
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
        expected = self._test_result('test_results.txt', 21, 23)
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
        expected = self._test_result('test_results.txt', 26, 38)
        self._test_print(func, data, expected)

    def test_run(self):
        """Test run() function."""
        pass


if __name__ == '__main__':
    unittest.main()
