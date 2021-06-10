from os.path import join
from unittest import TestCase
from unittest.mock import Mock, patch

from rootpath import detect

from modules.connector import Connector
from rss_reader.rss_reader.rss_reader import create_logger


def mock_response(status, content):
    """Function that simulate the response from requests.get"""

    class MockResponse:
        def __init__(self):
            self.raise_for_status = Mock()
            self.status_code = status
            self.content = content
            self.text = content

    return MockResponse()


file_path = join(detect(), 'rss_reader', 'data', 'example', 'page_without_rss.html')
with open(file_path, 'r') as file:
    data = file.read()


@patch('requests.get')
class TestConnector(TestCase):
    def setUp(self) -> None:
        self.logger = create_logger()

    def test_bad_url(self, mock_get):
        # mock_get.return_value(mock_response(200, data))
        mock_get.return_value = Mock()
        # mock_get.return_value.raise_for_status = Mock()
        mock_get.return_value.status = 500
        # mock_get.return_value.content = 'dada'
        mock_get.return_value.text = 'dada'
        with self.assertLogs(logger='root', level='ERROR') as logs:
            Connector(url='https://lenntta.ru/', logger=self.logger)
        self.assertIn('ERROR:root:Invalid URL. RSS feed not found.', logs.output)
