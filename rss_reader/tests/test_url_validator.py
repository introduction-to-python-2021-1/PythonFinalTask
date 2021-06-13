from unittest import TestCase

from rss_reader.src.modules.url_validator import RssUrlValidator
from rss_reader.src.rss_reader import create_logger


class TestUrlValidator(TestCase):

    def setUp(self) -> None:
        self.logger = create_logger()

    def test_get_status_code_success(self):
        validator = RssUrlValidator('https://lenta.ru/rss/news/', self.logger)
        status_code = validator.get_status_code()
        self.assertEqual(status_code, 200)

    def test_get_status_code_failure(self):
        status_code_1 = RssUrlValidator('https://lenta.ru/rss/nes/', self.logger).get_status_code()
        self.assertEqual(status_code_1, 404)
        status_code_2 = RssUrlValidator('htt://lenta.ru/rss/news/', self.logger).get_status_code()
        self.assertEqual(status_code_2, None)
        status_code_3 = RssUrlValidator('', self.logger).get_status_code()
        self.assertEqual(status_code_3, None)

    def test_get_validated_url_success(self):
        url = RssUrlValidator('https://lenta.ru/rss/news/', self.logger).get_validated_url()
        self.assertEqual(url, 'https://lenta.ru/rss/news/')

    def test_get_validated_url_failure(self):
        url = RssUrlValidator('https://lenta.u/rss/news/', self.logger).get_validated_url()
        self.assertEqual(url, '')
