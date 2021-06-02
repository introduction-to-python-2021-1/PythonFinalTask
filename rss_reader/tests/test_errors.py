import argparse
from io import StringIO
import logging
import os
import unittest
from unittest.mock import patch

from rss_reader.rss_reader import rss_reader


class TestRssReader(unittest.TestCase):
    @staticmethod
    def mock_response(status, content):
        """Function that simulate the response from requests.get"""
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.status_code = status
        mock_response.content = content
        return mock_response

    def test_wrong_url(self):
        """Tests that if specified invalid URL app should print error"""
        argv = ['https://pagethatdoesnexist.error/']
        with self.assertLogs('root', level='ERROR') as cm:
            rss_reader.main(argv)
        self.assertIn(
            'ERROR:root:An error occurred while sending a GET request to the specified URL. Check the specified URL'
            ' and your internet connection', cm.output)

    @patch('sys.stderr', new_callable=StringIO)
    def test_negative_limit(self, mock_stderr):
        """Tests that if --limit option is negative app should print error"""
        argv = ['https://news.yahoo.com/rss/', '--limit=-1']
        with self.assertRaises(SystemExit):
            with self.assertRaises(argparse.ArgumentTypeError):
                rss_reader.main(argv)
        self.assertIn('The limit argument must be greater than zero (-1 was passed)', mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_zero_limit(self, mock_stderr):
        """Tests that if --limit option is zero app should print error"""
        argv = ['https://news.yahoo.com/rss/', '--limit=0']
        with self.assertRaises(SystemExit):
            with self.assertRaises(argparse.ArgumentTypeError):
                rss_reader.main(argv)
        self.assertIn('The limit argument must be greater than zero (0 was passed)', mock_stderr.getvalue())

    def test_url_has_no_schema_supplied(self):
        """Tests that if specified URL has no schema supplied app should print error"""
        with self.assertLogs('root', level='ERROR') as cm:
            rss_reader.get_data_from_url(logging, 'url.com')
        self.assertIn(
            'ERROR:root:Invalid URL "url.com". The specified URL should look like "http://www.example.com/"',
            cm.output)

    @patch('requests.get')
    def test_url_does_not_contain_rss(self, mock_get):
        """Tests that if specified URL does not contain RSS app should print error"""
        data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')) + os.path.sep
        with open(data_folder + 'example_without_rss.html', 'r') as file:
            response_content = file.read()
        mock_response = self.mock_response(200, response_content)
        mock_get.return_value = mock_response
        with self.assertLogs('root', level='ERROR') as cm:
            rss_reader.get_data_from_url(logging, 'https://yahoo.com/rss/')
        self.assertIn('ERROR:root:Specified URL does not contain RSS. Please check the specified URL and try again',
                      cm.output)

    def test_url_not_specified(self):
        """Tests that if specified URL is empty app should print error"""
        argv = ['']
        with self.assertLogs('root', level='ERROR') as cm:
            rss_reader.main(argv)
        self.assertIn('ERROR:root:Source URL not specified. Please check your input and try again', cm.output)


if __name__ == '__main__':
    unittest.main()
