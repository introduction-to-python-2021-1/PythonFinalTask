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
