from unittest import TestCase

from src.modules.url_validator import RssUrlValidator
from src.rss_reader import create_logger


class TestUrlValidator(TestCase):

    def setUp(self) -> None:
        self.logger = create_logger()

    def test_get_status_code_success(self):
        status_code = RssUrlValidator('https://lenta.ru/rss/news/', self.logger).get_status_code()
        self.assertEqual(status_code, 200)

    def test_get_status_code_failure(self):
        status_code_1 = RssUrlValidator('https://lenta.ru/rss/nes/', self.logger).get_status_code()
        self.assertEqual(status_code_1, 404)
        status_code_2 = RssUrlValidator('htt://lenta.ru/rss/news/', self.logger).get_status_code()
        self.assertEqual(status_code_2, None)
        status_code_3 = RssUrlValidator('', self.logger).get_status_code()
        self.assertEqual(status_code_3, None)

    def test_validate_for_rss_success(self):
        rss_exists = RssUrlValidator('https://lenta.ru/rss/news/', self.logger).validate_for_rss()
        self.assertEqual(rss_exists, True)

    def test_validate_for_rss_failure(self):
        rss_exists = RssUrlValidator('htt://lenta.ru/rss/news/', self.logger).validate_for_rss()
        self.assertEqual(rss_exists, False)

    def test_get_validated_url_success(self):
        url = RssUrlValidator('https://lenta.ru/rss/news/', self.logger).get_validated_url()
        self.assertEqual(url, 'https://lenta.ru/rss/news/')

    def test_get_validated_url_failure(self):
        url = RssUrlValidator('https://lenta.u/rss/news/', self.logger).get_validated_url()
        self.assertEqual(url, '')
