import unittest
from unittest.mock import patch
from io import StringIO
import re
import json

from rss_reader.rss_reader.rss_reader import main


class TestRssReader(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_version(self, mock_stdout):
        """Tests that if --version option is specified app should just print its version and stop"""
        argv = ['--version']
        with self.assertRaises(SystemExit):
            main(argv)
        self.assertEqual(mock_stdout.getvalue(), 'Version 0.3\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_version_with_the_provided_source(self, mock_stdout):
        """Tests that if source URL and --version option is specified app should just print its version and stop"""
        argv = ['https://news.yahoo.com/rss/', '--version']
        with self.assertRaises(SystemExit):
            main(argv)
        self.assertEqual(mock_stdout.getvalue(), 'Version 0.3\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_limit(self, mock_stdout):
        """Tests that if --limit is specified user should get specified number of news"""
        argv = ['https://news.yahoo.com/rss/', '--limit=2']
        main(argv)
        result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', mock_stdout.getvalue())
        self.assertEqual(len(result_news_dates_and_links), 2)

    @patch('sys.stdout', new_callable=StringIO)
    def test_limit_larger_than_feed_size(self, mock_stdout):
        """Tests that if --limit is larger than feed size then user should get all available news"""
        argv = ['https://news.yahoo.com/rss/', '--limit=999']
        main(argv)
        result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', mock_stdout.getvalue())
        self.assertEqual(len(result_news_dates_and_links), 50)

    @patch('sys.stdout', new_callable=StringIO)
    def test_limit_is_not_specified(self, mock_stdout):
        """Tests that if --limit is not specified, then user should get all available feed"""
        argv = ['https://news.yahoo.com/rss/']
        main(argv)
        result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', mock_stdout.getvalue())
        self.assertEqual(len(result_news_dates_and_links), 50)

    @patch('sys.stdout', new_callable=StringIO)
    def test_json(self, mock_stdout):
        """Tests that if --json option is specified utility should convert the news into JSON format"""
        argv = ['https://news.yahoo.com/rss/', '--json']
        main(argv)
        try:
            json.loads(mock_stdout.getvalue())
        except json.JSONDecodeError:
            self.fail('JSONDecodeError raised by json.loads')

    @patch('sys.stdout', new_callable=StringIO)
    def test_json_with_limit(self, mock_stdout):
        """
        Tests that if --limit and --json option is specified utility should convert the news into JSON format
        and user should get specified number of news
        """
        argv = ['https://news.yahoo.com/rss/', '--limit=2', '--json']
        main(argv)
        try:
            result_json = json.loads(mock_stdout.getvalue())
        except json.JSONDecodeError:
            self.fail('JSONDecodeError raised by json.loads')
        else:
            self.assertEqual(len(result_json['0']['items']), 2)


if __name__ == '__main__':
    unittest.main()
