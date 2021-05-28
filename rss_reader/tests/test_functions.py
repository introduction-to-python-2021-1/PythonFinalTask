import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from urllib.error import URLError

from reader.functions import parse_news, make_json, check_limit, check_url, execute_news
from reader.article import Article


class TestFunctions(unittest.TestCase):
    """Test cases to test functions"""

    def setUp(self):
        self.url = 'Some_URL'
        self.article_A = Article('Japan reporter freed from Myanmar says inmates were abused',
                                 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html',
                                 '2021-05-21T15:03:25Z', 'Associated Press', '---',
                                 'https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAwMDthcHB'
                                 'pZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc')
        self.entries = [{'title': 'Japan reporter freed from Myanmar says inmates were abused',
                         'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://news.yahoo.com/rss/',
                                          'value': 'Japan reporter freed from Myanmar says inmates were abused'},
                         'links': [{'rel': 'alternate', 'type': 'text/html',
                                    'href': 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html'}],
                         'link': 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html',
                         'published': '2021-05-21T15:03:25Z',
                         'published_parsed': 'time.struct_time(tm_year=2021, tm_mon=5, tm_mday=21, tm_hour=8, tm_min=21'
                                             ', tm_sec=38, tm_wday=4, tm_yday=141, tm_isdst=0)',
                         'source': {'href': 'http://www.ap.org/', 'title': 'Associated Press'},
                         'id': 'japan-reporter-freed-myanmar-says-082138070.html', 'guidislink': False,
                         'media_content': [{'height': '86',
                                            'url': 'https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOT'
                                                   'k4O3c9MzAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.'
                                                   'org/d2d71e1fafaffbdd78bb05538e0732dc',
                                            'width': '130'}], 'media_credit': [{'role': 'publishing company'}],
                         'credit': ''}]

    @patch('reader.functions.store_news')
    def test_parse_news(self, store):
        """Checks that processing the entries creates an object of the Article class"""
        store.return_value = ''
        self.actual = parse_news(self.entries, None, None, self.url)[0]
        self.assertEqual(self.actual, self.article_A)

    @patch('reader.functions.store_news')
    def test_empty_news(self, store):
        """Checks that the program exits after recieving an empty input"""
        self.entries = {'entries': []}
        store.return_value = ''

        with self.assertRaises(SystemExit) as cm:
            parse_news(self.entries, None, None, self.url)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Sorry, no news to parse!")

    def test_make_json(self):
        """Checks that туцы is converted to json format correctly"""
        self.assertEqual(make_json(self.article_A),
                         '{\n    "Title": "Japan reporter freed from Myanmar says inmates were abused",\n'
                         '    "Link": "https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html",\n'
                         '    "Date": "Fri, 21 May, 2021",\n    "Source": "Associated Press",\n'
                         '    "Description": "---",\n'
                         '    "Image": "https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAw'
                         'MDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc"'
                         '\n}')

    def test_check_limit(self):
        """Tests check_limit function with valid values (positive numbers)"""
        self.assertEqual(check_limit('2'), 2)

    def test_check_limit_value_error(self):
        """Tests check_limit function with unvalid values (letters)"""
        with self.assertRaises(SystemExit) as cm:
            check_limit('symbol')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be a positive number')

    def test_check_limit_negative(self):
        """Tests check_limit function with unvalid values (negative numbers)"""
        with self.assertRaises(SystemExit) as cm:
            check_limit('-10')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be greater than 0')

    def test_check_limit_zero(self):
        """Tests check_limit function with unvalid values (zero)"""
        with self.assertRaises(SystemExit) as cm:
            check_limit('0')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be greater than 0')

    @patch('feedparser.parse')
    def test_bad_link(self, mock_api_call):
        """Tests check_url function if url returns empty news list"""
        mock_api_call.return_value = {'entries': []}
        with self.assertRaises(SystemExit) as cm:
            check_url(self.url, None, None)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Please, check if the entered link is correct!")

    @patch('feedparser.parse')
    def test_unvalid_url(self, mock_api_call):
        """Tests check_url function if url is not available"""
        mock_api_call.side_effect = MagicMock(side_effect=URLError('foo'))
        with self.assertRaises(SystemExit) as cm:
            check_url(self.url, None, None)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Source isn't available")

    @patch('reader.functions.store_news')
    @patch('feedparser.parse')
    def test_valid_url(self, parser, store):
        """Tests check_url function if url returns correct news list"""
        parser.return_value = {'entries': self.entries}
        store.return_value = ''

        self.actual = check_url(self.entries, None, None)
        self.assertEqual(self.actual[0], self.article_A)


if __name__ == "__main__":
    unittest.main()
