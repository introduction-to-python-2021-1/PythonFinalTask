import unittest
import argparse
import sqlite3

from reader.functions import parse_news, make_json, check_limit, execute_news, store_news
from reader.article import Article

connection = sqlite3.connect('news.db')
cursor = connection.cursor()

"""Test cases to test functions"""


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.article_A = Article('Japan reporter freed from Myanmar says inmates were abused',
                                 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html',
                                 '2021-05-21T15:03:25Z', 'Associated Press', '---',
                                 'https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAwMDthcHB'
                                 'pZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc')
        self.article_B = Article('Title_B',
                                 'Link_B',
                                 '2021-05-25T15:03:25Z', 'Source_B', '---',
                                 'Image_B')
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
        # self.empty_entries = [{}]

    def test_parse_news(self):
        self.actual = parse_news(self.entries, cursor, connection)[0]
        self.assertEqual(self.actual, self.article_A)

    # def test_parse_empty_news(self):
    #     self.actual = parse_news(self.empty_entries, cursor, connection)[0]
    #     self.assertEqual(self.actual, self.article_A)

    def test_make_json(self):
        self.assertEqual(make_json(self.article_A),
                         '{\n    "Title": "Japan reporter freed from Myanmar says inmates were abused",\n'
                         '    "Link": "https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html",\n'
                         '    "Date": "Fri, 21 May, 2021",\n    "Source": "Associated Press",\n'
                         '    "Description": "---",\n'
                         '    "Image": "https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAwMDthc'
                         'HBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc"\n}')

    def test_check_limit(self):
        self.assertEqual(check_limit('2'), 2)

    def test_check_limit_value_error(self):
        with self.assertRaises(SystemExit) as cm:
            check_limit('symbol')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be a positive number')

    def test_check_limit_negative(self):
        with self.assertRaises(SystemExit) as cm:
            check_limit('-10')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be greater than 0')

    def test_check_limit_zero(self):
        with self.assertRaises(SystemExit) as cm:
            check_limit('0')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be greater than 0')


if __name__ == "__main__":
    unittest.main()
