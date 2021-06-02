from bs4 import BeautifulSoup

from rss_reader.tests.testing import BaseTest


class TestConverter(BaseTest):
    def test_to_html(self):
        """Tests that html is generated"""
        result_html = self.converter.to_html([self.example_feed], None, pdf=True, output_filepath='test.pdf')
        document_data = BeautifulSoup(result_html, 'lxml')
        self.assertEqual(len(document_data.find_all('div')), 5)

    def test_to_html_with_limit(self):
        """Tests that the --limit argument affects the number of news in html"""
        result_html = self.converter.to_html([self.example_feed], 2, pdf=True, output_filepath='test.pdf')
        document_data = BeautifulSoup(result_html, 'lxml')
        self.assertEqual(len(document_data.find_all('div')), 2)
