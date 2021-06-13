from unittest import TestCase
from unittest.mock import patch

from rss_reader.src.modules.rss_parser import RSSParser
from rss_reader.src.rss_reader import create_logger

rss_channel = """
<rss xmlns:media="https://search.yahoo.com/mrss/" version="2.0">
    <channel>
        <title>Yahoo News - Latest News & Headlines</title>
        <link>https://www.yahoo.com/news</link>
        <description>The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage
         with videos and photos.</description>
        <language>en-US</language>
        <copyright>Copyright (c) 2021 Yahoo! Inc. All rights reserved</copyright>
        <pubDate>Fri, 11 Jun 2021 09:22:10 -0400</pubDate>
        <ttl>5</ttl>
        <image>
            <title>Yahoo News - Latest News & Headlines</title>
            <link>https://www.yahoo.com/news</link>
            <url>https://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png</url>
        </image>
        <item>
            <title>Undervaccinated red states are nowhere near herd immunity as dangerous Delta variant spreads</title>
            <link>https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as-dangerous-
                  delta-variant-spreads-090052183.html
            </link>
            <pubDate>2021-06-11T09:00:52Z</pubDate>
            <source url="https://news.yahoo.com/">Yahoo News</source>
            <guid isPermaLink="false">undervaccinated-red-states-are-nowhere-near-herd-immunity-as-
            dangerous-delta-variant-spreads-090052183.html
            </guid>
            <media:content height="86" url="https://s.yimg.com/os/creatr-uploaded-images/2021-06/1393bb40-ca2d-
            11eb-bddf-ea9188da9f73" width="130"/>
            <media:credit role="publishing company"/>
        </item>
    </channel>
</rss>"""

result = r"""{'bozo': 1,
 'bozo_exception': SAXParseException('not well-formed (invalid token)'),
 'encoding': 'utf-8',
 'entries': [{'credit': '',
              'guidislink': False,
              'id': 'undervaccinated-red-states-are-nowhere-near-herd-immunity-as-\n'
                    '            '
                    'dangerous-delta-variant-spreads-090052183.html',
              'link': 'https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as-dangerous-\n'
                      '                  delta-variant-spreads-090052183.html',
              'links': [{'href': 'https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as-dangerous-\n'
                                 '                  '
                                 'delta-variant-spreads-090052183.html',
                         'rel': 'alternate',
                         'type': 'text/html'}],
              'media_content': [{'height': '86',
                                 'url': 'https://s.yimg.com/os/creatr-uploaded-images/2021-06/1393bb40-ca2d-\n'
                                        '            11eb-bddf-ea9188da9f73',
                                 'width': '130'}],
              'media_credit': [{'role': 'publishing company'}],
              'published': '2021-06-11T09:00:52Z',
              'published_parsed': time.struct_time(tm_year=2021, tm_mon=6, tm_mday=11, tm_hour=9, tm_min=0, tm_sec=52, tm_wday=4, tm_yday=162, tm_isdst=0),
              'source': {'href': 'https://news.yahoo.com/',
                         'title': 'Yahoo News'},
              'title': 'Undervaccinated red states are nowhere near herd '
                       'immunity as dangerous Delta variant spreads',
              'title_detail': {'base': '',
                               'language': None,
                               'type': 'text/plain',
                               'value': 'Undervaccinated red states are '
                                        'nowhere near herd immunity as '
                                        'dangerous Delta variant spreads'}}],
 'feed': {'image': {'href': 'https://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png',
                    'link': 'https://www.yahoo.com/news',
                    'links': [{'href': 'https://www.yahoo.com/news',
                               'rel': 'alternate',
                               'type': 'text/html'}],
                    'title': 'Yahoo News - Latest News & Headlines',
                    'title_detail': {'base': '',
                                     'language': None,
                                     'type': 'text/plain',
                                     'value': 'Yahoo News - Latest News & '
                                              'Headlines'}},
          'language': 'en-US',
          'link': 'https://www.yahoo.com/news',
          'links': [{'href': 'https://www.yahoo.com/news',
                     'rel': 'alternate',
                     'type': 'text/html'}],
          'published': 'Fri, 11 Jun 2021 09:22:10 -0400',
          'published_parsed': time.struct_time(tm_year=2021, tm_mon=6, tm_mday=11, tm_hour=13, tm_min=22, tm_sec=10, tm_wday=4, tm_yday=162, tm_isdst=0),
          'rights': 'Copyright (c) 2021 Yahoo! Inc. All rights reserved',
          'rights_detail': {'base': '',
                            'language': None,
                            'type': 'text/plain',
                            'value': 'Copyright (c) 2021 Yahoo! Inc. All '
                                     'rights reserved'},
          'subtitle': 'The latest news and headlines from Yahoo! News. Get '
                      'breaking news stories and in-depth coverage\n'
                      '         with videos and photos.',
          'subtitle_detail': {'base': '',
                              'language': None,
                              'type': 'text/html',
                              'value': 'The latest news and headlines from '
                                       'Yahoo! News. Get breaking news stories '
                                       'and in-depth coverage\n'
                                       '         with videos and photos.'},
          'title': 'Yahoo News - Latest News & Headlines',
          'title_detail': {'base': '',
                           'language': None,
                           'type': 'text/plain',
                           'value': 'Yahoo News - Latest News & Headlines'},
          'ttl': '5'},
 'headers': {},
 'namespaces': {'media': 'https://search.yahoo.com/mrss/'},
 'version': 'rss20'}"""


class TestRssParser(TestCase):

    def setUp(self) -> None:
        self.logger = create_logger()

    def test_get_rss_channel(self):
        channel = RSSParser(rss_channel, self.logger, 1).get_rss_channel()
        self.assertEqual(channel, result)

