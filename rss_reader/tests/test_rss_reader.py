import unittest
from io import StringIO
from unittest.mock import patch

from modules.connector import Connector
from modules.rssparser import RSSparser
from rss_reader.rss_reader.rss_reader import main, VERSION, create_logger

logger = create_logger()
URL_BAD = 'https://www.dsfsdfsdf.com/'
URL_WITH_RSS = 'https://news.yahoo.com/rss/'
URL_WITHOUT_RSS = 'https://news.yahoo.com/'


class TestMain(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_version(self, mock_stdout):
        argv = ['None', '--version']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), '\nVersion {}\n'.format(VERSION))

    @patch('sys.stdout', new_callable=StringIO)
    def test_version_with_source(self, mock_stdout):
        argv = ['None', 'https://news.yahoo.com/rss/', '--version']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), '\nVersion {}\n'.format(VERSION))

    def test_bad_url(self):
        with self.assertLogs('root', level='ERROR') as logs:
            main(['None', URL_BAD])
        self.assertIn('ERROR:root:Connection not detected.', logs.output)


class TestConnector(unittest.TestCase):

    def test_bad_url(self):
        self.assertEqual(Connector(URL_BAD, logger).is_connect, False)

    def test_url_without_rss(self):
        self.assertEqual(Connector(URL_WITHOUT_RSS, logger).is_connect, False)

    def test_url_with_rss(self):
        self.assertEqual(Connector(URL_WITH_RSS, logger).is_connect, True)


class TestRSSparser(unittest.TestCase):
    URL = 'https://news.yahoo.com/rss/'

    def test_limit_more_news(self):
        news = RSSparser(self.URL, logger, limit=9999)
        self.assertEqual(news.limit, news.news_count)

    def test_negative_limit(self):
        news = RSSparser(self.URL, logger, limit=-9999)
        self.assertEqual(news.limit, news.news_count)


if __name__ == '__main__':
    unittest.main()
