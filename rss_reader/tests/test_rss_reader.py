# Author: Julia Los <los.julia.v@gmail.com>.

"""Test command-line RSS reader."""

import feedparser
import unittest

from io import StringIO
from rss_reader.rss_reader.rss_reader import parse_url, format_date, get_image_link, load_data
from rss_reader.rss_reader.rss_reader import colorize_text, print_as_formatted_text, print_as_json
from time import strptime
from unittest.mock import patch

_test_data_xml_filename = r'tests/test_rss.xml'
_test_data_json_filename = r'tests/test_storage.json'
_test_results_txt_filename = r'tests/test_results.txt'


class RSSReaderTests(unittest.TestCase):
    """Test functions of RSSReader class."""

    def test_parse_url_for_None(self):
        """Test parse_url() function for None."""
        with self.assertRaises(SystemExit):
            parse_url(None)

    def test_parse_url_for_empty_url(self):
        """Test parse_url() function for empty url."""
        with self.assertRaises(SystemExit):
            parse_url('')

    def test_parse_url_for_incorrect_url(self):
        """Test parse_url() function for correct url."""
        self.assertIsNotNone(parse_url('https://www.wikipedia.org/'))

    def test_parse_url_for_correct_url(self):
        """Test parse_url() function for correct url."""
        self.assertIsNotNone(parse_url('https://news.yahoo.com/rss/'))

    def test_format_date_for_None(self):
        """Test format_date() function for None."""
        self.assertEqual(format_date(None, '%a, %d %b, %Y %I:%M %p'), '')

    def test_format_date_for_int(self):
        """Test format_date() function for int."""
        self.assertEqual(format_date(5, '%a, %d %b, %Y %I:%M %p'), '')

    def test_format_date_for_incorrect_string(self):
        """Test format_date() function for incorrect string."""
        self.assertEqual(format_date("Error date", '%a, %d %b, %Y %I:%M %p'), '')

    def test_format_date_for_correct_string(self):
        """Test format_date() function for correct string."""
        self.assertEqual(format_date(strptime('Sun, 23 May, 2021 05:30 PM', '%a, %d %b, %Y %I:%M %p'),
                                     '%a, %d %b, %Y %I:%M %p'), 'Sun, 23 May, 2021 05:30 PM')

    def test_get_image_link_for_enclosure_tag(self):
        """Test get_image_link() function for <enclosure> tag."""
        parser = feedparser.parse("""<item><enclosure url="http://test.com/image.jpg" type="image/jpeg"/></item>""")
        self.assertEqual(get_image_link(parser.entries[0]), 'http://test.com/image.jpg')

    def test_get_image_link_for_figure_tag(self):
        """Test get_image_link() function for <figure> tag."""
        parser = feedparser.parse("""<item><figure><img src="http://test.com/image.jpg"></figure></item>)""")
        self.assertEqual(get_image_link(parser.entries[0]), 'http://test.com/image.jpg')

    def test_get_image_link_for_media_content_tag(self):
        """Test get_image_link() function for <media:content> tag."""
        parser = feedparser.parse("""<item><media:content url="http://test.com/image.jpg"/></item>)""")
        self.assertEqual(get_image_link(parser.entries[0]), 'http://test.com/image.jpg')

    def test_load_data_for_None(self):
        """Test load_date() function for None."""
        self.assertIsNone(load_data(None, ''))

    def test_load_data_for_empty_channel(self):
        """Test load_date() function for empty channel."""
        parser = feedparser.parse('')
        self.assertIsNone(load_data(parser, ''))

    def test_load_data_for_full_data(self):
        """Test load_date() function for full data."""
        parser = feedparser.parse(_test_data_xml_filename)
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
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'image': '',
                      'description': ''},
                 ]}]
        self.assertEqual(load_data(parser, 'https://news.ru/'), data)

    def test_colorize_text_for_off_colorize_mode(self):
        """Test colorize_text() function for off colorize mode."""
        self.assertEqual(colorize_text(False, 'test_word', 'blue'), 'test_word')

    def test_colorize_text_for_incorrect_text_color(self):
        """Test colorize_text() function for incorrect text color."""
        self.assertEqual(colorize_text(True, 'test_word', 'black'), 'test_word')

    def test_colorize_text_for_correct_text_color(self):
        """Test colorize_text() function for correct text color."""
        self.assertEqual(colorize_text(True, 'test_word', 'blue'), '\033[34mtest_word\033[0m')

    def test_colorize_text_for_incorrect_background_color(self):
        """Test colorize_text() function for incorrect background color."""
        self.assertEqual(colorize_text(True, 'test_word', 'blue', 'on_black'), 'test_word')

    def test_colorize_text_for_correct_background_color(self):
        """Test colorize_text() function for correct background color."""
        self.assertEqual(colorize_text(True, 'test_word', 'blue', 'on_white'), '\033[47m\033[34mtest_word\033[0m')

    def test_colorize_text_for_incorrect_keyword_for_attributes(self):
        """Test colorize_text() function for incorrect keyword for attributes."""
        self.assertEqual(colorize_text(True, 'test_word', 'blue', attributes=['bold']), 'test_word')

    def test_colorize_text_for_incorrect_attributes(self):
        """Test colorize_text() function for incorrect attributes."""
        self.assertEqual(colorize_text(True, 'test_word', 'blue', attrs=['b-o-l-d']), 'test_word')

    def test_colorize_text_for_correct_attributes(self):
        """Test colorize_text() function for correct attributes."""
        self.assertEqual(colorize_text(True, 'test_word', 'blue', attrs=['bold']), '\x1b[1m\x1b[34mtest_word\x1b[0m')

    @staticmethod
    def _test_result(filename, beg_line=0, end_line=None):
        """Read data from file."""
        with open(filename, 'r', encoding="utf-8") as f:
            result = f.readlines()
        if end_line:
            return "".join(result[beg_line:end_line + 1])
        else:
            return "".join(result[beg_line:])

    def _test_print(self, expected, func, data, is_colorize=False):
        """Write data to fake output."""
        with patch('sys.stdout', new=StringIO()) as test_out:
            func(data, is_colorize)
            self.assertEqual(test_out.getvalue(), expected)

    def test_print_as_formatted_text_for_None(self):
        """Test print_as_formatted_text() function for None."""
        self._test_print('', print_as_formatted_text, None)

    def test_print_as_formatted_text_for_empty_data(self):
        """Test print_as_formatted_text() function for empty data."""
        self._test_print('', print_as_formatted_text, {})

    def test_print_as_formatted_text_for_only_channel(self):
        """Test print_as_formatted_text() function for only channel."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel'}]
        expected = self._test_result(_test_results_txt_filename, 1, 2)
        self._test_print(expected, print_as_formatted_text, data)

    def test_print_as_formatted_text_for_full_data(self):
        """Test print_as_formatted_text() function for full data."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Sun, 23 May, 2021 05:30 PM',
                      'image': 'http://test.com/image.jpg',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'image': '',
                      'description': ''},
                 ]}]
        expected = self._test_result(_test_results_txt_filename, 5, 18)
        self._test_print(expected, print_as_formatted_text, data)

    def test_print_as_formatted_text_for_full_data_for_colorize_mode(self):
        """Test print_as_formatted_text() function for full data for colorize mode."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Sun, 23 May, 2021 05:30 PM',
                      'image': 'http://test.com/image.jpg',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'image': '',
                      'description': ''},
                 ]}]
        expected = self._test_result(_test_results_txt_filename, 21, 34)
        self._test_print(expected, print_as_formatted_text, data, True)

    def test_print_as_json_for_None(self):
        """Test print_as_json() function for None."""
        self._test_print('', print_as_json, None)

    def test_print_as_json_for_empty_data(self):
        """Test print_as_json() function for empty data."""
        self._test_print('', print_as_json, {})

    def test_print_as_json_for_only_channel(self):
        """Test print_as_json() function for only channel."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel'}]
        expected = self._test_result(_test_results_txt_filename, 37, 42)
        self._test_print(expected, print_as_json, data)

    def test_print_as_json_for_full_data(self):
        """Test print_as_json() function for full data."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Sun, 23 May, 2021 05:30 PM',
                      'image': 'http://test.com/image.jpg',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'image': '',
                      'description': ''},
                 ]}]
        expected = self._test_result(_test_results_txt_filename, 45, 70)
        self._test_print(expected, print_as_json, data)

    def test_print_as_json_for_full_data_in_colorize_mode(self):
        """Test print_as_json() function for full data in colorize mode."""
        data = [{'channel_id': 'https://news.ru/',
                 'channel_title': 'News channel',
                 'news': [
                     {'number': 1,
                      'title': 'Last news',
                      'link': 'https://news.ru/last_news.html',
                      'author': 'Alexey Morozov',
                      'date': 'Sun, 23 May, 2021 05:30 PM',
                      'image': 'http://test.com/image.jpg',
                      'description': 'Last news'},
                     {'number': 2,
                      'title': 'Next news',
                      'link': 'https://super_news.ru/next_news.html',
                      'author': '',
                      'date': '',
                      'image': '',
                      'description': ''},
                 ]}]
        expected = self._test_result(_test_results_txt_filename, 73, 98)
        self._test_print(expected, print_as_json, data, True)


if __name__ == '__main__':
    unittest.main()
