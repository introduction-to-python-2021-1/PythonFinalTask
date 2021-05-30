"""
    This module covers with tests code of news_processor.py
"""
import unittest
from ddt import ddt, data
from io import StringIO
from unittest.mock import patch, MagicMock
from rss_core.news_processor import NewsProcessor
from rss_core.parser import XmlParser
from rss_core.reader import SiteReader
from rss_core.rss_classes import RssNews, RssItem

RSSNESW_DICT = {
    "Link": "Chanel link",
    "Description": "Chanel description",
    "Title": "Chanel title",
    "News": [
        {
            "Title": "News title",
            "Date": "News date",
            "Link": "News link",
            "Media": [
                "Media url"
            ]
        }
    ]
}

RSSNESW_ARRAY = [{
    "link": "Chanel link",
    "description": "Chanel description",
    "title": "Chanel title",
    "news": [
        RssItem(**{
            "title": "News1 title",
            "date": "News1 date",
            "link": "News1 link"
        }),
        RssItem(**{
            "title": "News1 title",
            "date": "News1 date",
            "link": "News1 link"
        })
    ]}, {
    "link": "Chanel link2",
    "description": "Chanel description2",
    "title": "Chanel title2",
    "news": [
        RssItem(**{
            "title": "News2 title",
            "date": "News2 date",
            "link": "News2 link"
        }),
        RssItem(**{
            "title": "News2 title",
            "date": "News2 date",
            "link": "News2 link"
        })
    ]}
]


@ddt
class TestNewsProcessor(unittest.TestCase):
    """
    Test NewsProcessor
    """

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_news_empty_link(self, mock_stdout):
        """
        Parse news from empty link
        """
        proc = NewsProcessor(XmlParser(SiteReader()))
        with self.assertRaises(SystemExit) as cm:
            proc.load_news("")
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual("[ERROR] Link mast be not empty str", mock_stdout.getvalue().strip())

    @patch('sys.stdout', new_callable=StringIO)
    def test_load_news_without_cacher(self, mock_stdout):
        """
        Parse news from empty link
        """
        XmlParser.parse_news = MagicMock(return_value=RSSNESW_DICT)
        proc = NewsProcessor(XmlParser(SiteReader()))
        proc.load_news("http://aaa")
        self.assertEqual("[WARNING] Cacher is not initialized. Cache won't be create!", mock_stdout.getvalue().strip())

    @patch('sys.stdout', new_callable=StringIO)
    def test_save_as_html_into_wrong_file(self, mock_stdout):
        """
        Test attempt to save html news into hdf file
        :return:
        """
        proc = NewsProcessor(XmlParser(SiteReader()))
        proc.save_news_as_html(output_to="a.pdf")
        self.assertEqual("[ERROR] Error has occurred while converting news to html: File should be in 'html' format",
                         mock_stdout.getvalue().replace("\n", ""))

    @patch('sys.stdout', new_callable=StringIO)
    def test_save_as_pdf_into_wrong_file(self, mock_stdout):
        proc = NewsProcessor(XmlParser(SiteReader()))
        proc.save_news_as_pdf(output_to="a.html")
        self.assertEqual("[ERROR] Error has occurred while converting news to html: File should be in 'pdf' format",
                         mock_stdout.getvalue().replace("\n", ""))

    @data([None, 2, 2], [3, 2, 1])
    def test_get_news_as_json(self, value):
        """
        Test getting news as json without limit
        """
        limit, news_channel1, news_channel2 = value
        proc = NewsProcessor(XmlParser(SiteReader()))
        proc.news = [RssNews(**rss_dict) for rss_dict in RSSNESW_ARRAY]
        json_rss = proc.get_news_as_json(limit)
        self.assertEqual(len(json_rss[0]["News"]), news_channel1)
        self.assertEqual(len(json_rss[1]["News"]), news_channel2)

    @data([None, 2, 2], [3, 2, 1])
    def test_get_news_as_str_limit(self, value):
        """
        Test limit behaviour while getting news as str
        """
        limit, news_channel1, news_channel2 = value
        proc = NewsProcessor(XmlParser(SiteReader()))
        proc.news = [RssNews(**rss_dict) for rss_dict in RSSNESW_ARRAY]
        str_rss = proc.get_news_as_str(limit)
        self.assertEqual(str_rss.count("News1 title"), news_channel1)
        self.assertEqual(str_rss.count("News2 title"), news_channel2)
