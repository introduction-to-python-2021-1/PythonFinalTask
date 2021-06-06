import filecmp
import os
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from rss_reader.rss_reader import rss_reader
from rss_reader.tests.testing import mock_response


@patch('requests.get')
class TestConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This method initializes variables used in tests"""
        cls.data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')) + os.path.sep
        with open(cls.data_folder + 'example.xml', 'r') as file:
            cls.document_content = file.read()

    def test_to_html(self, mock_get):
        """Tests that HTML is correctly generated and saved to a file"""
        mock_get.return_value = mock_response(200, self.document_content)
        argv = ['https://news.yahoo.com/rss/', '--to-html=test.html']
        rss_reader.main(argv)
        with open('test.html', 'r') as file:
            result_data = BeautifulSoup(file, 'lxml-xml')
        self.assertEqual(len(result_data.find_all('div')), 5)
        os.remove('test.html')

    def test_to_html_with_limit(self, mock_get):
        """Tests that the --limit argument affects the number of news in HTML"""
        mock_get.return_value = mock_response(200, self.document_content)
        argv = ['https://news.yahoo.com/rss/', '--to-html=test.html', '--limit=2']
        rss_reader.main(argv)
        with open('test.html', 'r') as file:
            result_data = BeautifulSoup(file, 'lxml-xml')
        self.assertEqual(len(result_data.find_all('div')), 2)
        os.remove('test.html')

    def test_to_pdf(self, mock_get):
        """Tests that PDF is saved to a file"""
        mock_get.return_value = mock_response(200, self.document_content)
        argv = ['https://news.yahoo.com/rss/', '--to-pdf=test.pdf']
        rss_reader.main(argv)
        self.assertTrue(os.path.exists('test.pdf'))
        os.remove('test.pdf')
