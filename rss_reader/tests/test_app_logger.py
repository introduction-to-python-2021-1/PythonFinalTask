from unittest import TestCase
from rss_reader import app_logger


class TestAppLogger(TestCase):

    def test_logger_link_test(self):
        logger1 = app_logger.get_logger(__name__)
        logger2 = app_logger.get_logger(__name__)
        self.assertEqual(logger1, logger2)

    def test_logger_file_handler(self):
        logger1 = app_logger.get_logger(__name__)
        logger2 = app_logger.get_logger(__name__)
        self.assertEqual(logger1.handlers[0], logger2.handlers[0])

    def test_logger_stream_handler(self):
        logger1 = app_logger.get_logger(__name__)
        logger2 = app_logger.get_logger(__name__)
        self.assertEqual(logger1.handlers[1], logger2.handlers[1])
