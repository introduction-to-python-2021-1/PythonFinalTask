import argparse
from io import StringIO
import unittest
from unittest.mock import patch

from rss_reader.rss_reader.rss_reader import main


class TestRssReader(unittest.TestCase):
    def test_wrong_url(self):
        """Tests that if specified invalid URL app should print error"""
        argv = ['https://pagethatdoesnexist.error/']
        with self.assertLogs('root', level='ERROR') as cm:
            main(argv)
        self.assertIn(
            'ERROR:root: An error occurred while sending a GET request to the specified URL. Check the specified URL'
            ' and your internet connection', cm.output)

    @patch('sys.stderr', new_callable=StringIO)
    def test_negative_limit(self, mock_stderr):
        """Tests that if --limit option is negative app should print error"""
        argv = ['https://news.yahoo.com/rss/', '--limit=-1']
        with self.assertRaises(SystemExit):
            with self.assertRaises(argparse.ArgumentTypeError):
                main(argv)
        self.assertIn('The limit argument must be greater than zero (-1 was passed)', mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_zero_limit(self, mock_stderr):
        """Tests that if --limit option is zero app should print error"""
        argv = ['https://news.yahoo.com/rss/', '--limit=0']
        with self.assertRaises(SystemExit):
            with self.assertRaises(argparse.ArgumentTypeError):
                main(argv)
        self.assertIn('The limit argument must be greater than zero (0 was passed)', mock_stderr.getvalue())

    def test_url_has_no_schema_supplied(self):
        """Tests that if specified URL has no schema supplied app should print error"""
        argv = ['url.com']
        with self.assertLogs('root', level='ERROR') as cm:
            main(argv)
        self.assertIn(
            'ERROR:root: Invalid URL "url.com". The specified URL should look like "http://www.example.com/"',
            cm.output)

    def test_url_does_not_contain_rss(self):
        """Tests that if specified URL does not contain RSS app should print error"""
        argv = ['https://yahoo.com/rss/']
        with self.assertLogs('root', level='ERROR') as cm:
            main(argv)
        self.assertIn('ERROR:root: Specified URL does not contain RSS. Please check the specified URL and try again',
                      cm.output)

    def test_url_not_specified(self):
        """Tests that if specified URL is empty app should print error"""
        argv = ['']
        with self.assertLogs('root', level='ERROR') as cm:
            main(argv)
        self.assertIn('ERROR:root: Source URL not specified. Please check your input and try again', cm.output)


if __name__ == '__main__':
    unittest.main()
