import io
from contextlib import redirect_stdout
from unittest.mock import patch
import unittest

from reader.rss_reader import main
from reader.article import Article


class TestMain(unittest.TestCase):

    def setUp(self):
        self.url = 'Some_URL'
        self.article_a = Article('Japan reporter freed from Myanmar says inmates were abused',
                                 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html',
                                 '2021-05-28T15:03:25Z', 'Associated Press', '---',
                                 'https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAwMDthcHB'
                                 'pZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc')
        self.entries = [{'title': 'Japan reporter freed from Myanmar says inmates were abused',
                         'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://news.yahoo.com/rss/',
                                          'value': 'Japan reporter freed from Myanmar says inmates were abused'},
                         'links': [{'rel': 'alternate', 'type': 'text/html',
                                    'href': 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html'}],
                         'link': 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html',
                         'published': '2021-05-28T15:03:25Z',
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
        self.json = '{\n    "Title": "Japan reporter freed from Myanmar says inmates were abused",\n' \
                    '    "Link": "https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html",\n' \
                    '    "Date": "Fri, 28 May, 2021",\n' \
                    '    "Source": "Associated Press",\n' \
                    '    "Description": "---",\n' \
                    '    "Image": "https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAw' \
                    'MDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc"\n}'

    @patch('feedparser.parse')
    def test_json_conversion(self, parser):
        """Checks that the program converts the news into JSON format when --json is specified"""
        parser.return_value = {'entries': self.entries}
        with io.StringIO() as term_value, redirect_stdout(term_value):
            main([None, self.url, '--json'])
            self.assertEqual(term_value.getvalue(), self.json + '\n')

    @patch('reader.functions.execute_news')
    def test_news_for_specific_date(self, store):
        """Checks that the program returns news for a given date if --date is specified"""
        store.return_value = [self.article_a]
        with io.StringIO() as term_value, redirect_stdout(term_value):
            main([None, self.url, '--date', '20210528'])
            self.assertEqual(term_value.getvalue(), self.article_a.__str__() + '\n')

    @patch('reader.functions.execute_news')
    def test_news_for_nonexistent_date(self, store):
        """Checks that the program returns no news for a nonexistent date if --date is specified"""
        store.return_value = []
        with self.assertRaises(SystemExit) as cm:
            main([None, self.url, '--date', '20210521'])

        self.actual = cm.exception.args[0]
        self.assertEqual(self.actual, 'Sorry, there are no articles for 2021-05-21!')

    def test_invalid_date(self):
        """Checks that the program displays a message if --date is is specified in the wrong format"""
        with self.assertRaises(SystemExit) as cm:
            main([None, self.url, '--date', '202105281'])

        self.actual = cm.exception.args[0]
        self.assertEqual(self.actual, 'Please, enter the date in the following format: "YYYYMMDD".')

    @patch('reader.functions.execute_news')
    def test_date_plus_json_conversion(self, store):
        """Checks that the program returns news for a given date in json format if --date and --json are specified"""
        store.return_value = [self.article_a]
        with io.StringIO() as term_value, redirect_stdout(term_value):
            main([None, self.url, '--date', '20210528', '--json'])
            self.assertEqual(term_value.getvalue(), self.json + '\n')

    @patch('reader.functions.execute_news')
    def test_date_plus_limit(self, store):
        """Checks that program returns news for a given date in a given limit if --date and --limit are specified"""
        store.return_value = [self.article_a, self.article_a]
        with io.StringIO() as term_value, redirect_stdout(term_value):
            main([None, self.url, '--date', '20210528', '--limit', '1'])
            self.assertEqual(term_value.getvalue(), self.article_a.__str__() + '\n')
