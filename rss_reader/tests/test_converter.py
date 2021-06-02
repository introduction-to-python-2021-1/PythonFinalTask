import filecmp
import os

from bs4 import BeautifulSoup

from rss_reader.tests.testing import BaseTest


class TestConverter(BaseTest):
    def test_to_html(self):
        """Tests that html is generated and saved to a file"""
        self.converter.to_html([self.example_feed], None, os.path.dirname(__file__) + os.sep + 'test.html')
        self.assertTrue(
            filecmp.cmp(os.path.dirname(__file__) + os.sep + 'test.html', self.data_folder + 'result_html.html'))
        os.remove(os.path.dirname(__file__) + os.sep + 'test.html')

    def test_to_html_with_limit(self):
        """Tests that the --limit argument affects the number of news in html"""
        result_html = self.converter.to_html([self.example_feed], 2, pdf=True, output_filepath='test.pdf')
        document_data = BeautifulSoup(result_html, 'lxml')
        self.assertEqual(len(document_data.find_all('div')), 2)
