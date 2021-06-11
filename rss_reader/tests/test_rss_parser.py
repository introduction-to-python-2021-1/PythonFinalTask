from unittest import TestCase
from unittest.mock import patch

from src.rss_reader import create_logger

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


class TestRssParser(TestCase):

    def setUp(self) -> None:
        self.logger = create_logger()

    @patch('src.modules.rss_parser.RSSParser')
    def test_parse(self, MockRSSParser):
        rss_parser = MockRSSParser(rss_channel, self.logger, 1)
        rss_parser.parse.return_value = [
            {
                'new 0': {
                    'feed': 'Yahoo News - Latest News & Headlines',
                    'title': 'Undervaccinated red states are nowhere near herd immunity as dangerous Delta variant'
                             ' spreads',
                    'date': '2021-06-11T09:00:52Z',
                    'link': 'https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as'
                            '-dangerous-delta-variant-spreads-090052183.html',
                    'links': {
                        'link 0': {
                            'href': 'https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-'
                                    'immunity-as-dangerous-delta-variant-spreads-090052183.html',
                            'type': 'text/html'
                        }
                    }
                }
            }
        ]
        response = rss_parser.parse()
        self.assertEqual(response, rss_parser.parse.return_value)
