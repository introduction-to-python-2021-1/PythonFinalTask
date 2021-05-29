import io
from contextlib import redirect_stdout
from unittest.mock import patch
import unittest

from reader.rss_reader import main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.url = 'Some_URL'
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
        self.json = '{\n    "Title": "Japan reporter freed from Myanmar says inmates were abused",\n' \
                    '    "Link": "https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html",\n' \
                    '    "Date": "Fri, 21 May, 2021",\n' \
                    '    "Source": "Associated Press",\n' \
                    '    "Description": "---",\n' \
                    '    "Image": "https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAw' \
                    'MDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc"\n}'

    @patch('feedparser.parse')
    def test_json_conversion(self, parser):
        """Checks that the program converts the news into JSON format when --json is specified"""
        parser.return_value = {'entries': self.entries}
        with io.StringIO() as term_value, redirect_stdout(term_value):
            main({'json': True, 'source': self.url})
            self.assertEqual(term_value.getvalue(), self.json + '\n')
