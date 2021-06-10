from os.path import join
from unittest import TestCase
from unittest.mock import Mock, patch

from rootpath import detect

from modules.connector import Connector
from rss_reader.rss_reader.rss_reader import create_logger

example_dir = join(detect(), 'rss_reader', 'data', 'example')
bad_example_path = join(example_dir, 'page_without_rss.html')
good_example_path = join(example_dir, 'news.xml')
with open(bad_example_path, 'r') as file:
    bad_data = file.read()

with open(good_example_path, 'r') as file:
    good_data = file.read()


class TestConnector(TestCase):
    def setUp(self) -> None:
        self.logger = create_logger()

    def test_bad_url(self):
        with self.assertLogs(logger='root', level='ERROR') as logs:
            Connector(url='https://www.lenntta.ru/', logger=self.logger)
        self.assertIn('ERROR:root:Connection not detected.', logs.output)

    @patch('requests.get')
    def test_url_without_rss(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.status = 200
        mock_get.return_value.text = bad_data
        with self.assertLogs(logger='root', level='ERROR') as logs:
            Connector(url='https://www.google.com/', logger=self.logger)
        self.assertIn('ERROR:root:Invalid URL. RSS feed not found.', logs.output)

    @patch('requests.get')
    def test_url_with_rss(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.status = 200
        mock_get.return_value.text = good_data
        self.assertEqual(Connector(url='https://lenta.ru/rss/news', logger=self.logger).response_text, good_data)
