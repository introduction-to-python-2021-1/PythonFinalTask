import io
import sys
import unittest
import logging
from rss_reader import reader
from rss_reader import app_logger


class TestMain(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        sys.stdout = self.output

    def test_version(self):
        argv = ["--version"]
        with self.assertRaises(SystemExit):
            reader.main(argv)

    def test_version_with_url(self):
        argv = ["https://news.yahoo.com/rss/", "--version"]
        with self.assertRaises(SystemExit):
            reader.main(argv)

    def test_limit_less_zero(self):
        argv = ["https://news.yahoo.com/rss/", "--limit", "-24"]
        with self.assertRaises(SystemExit):
            reader.main(argv)

    def test_uncorrect_json(self):
        argv = ["https://news.yahoo.com/rss/", "--json", "24"]
        with self.assertRaises(SystemExit):
            reader.main(argv)

    def test_uncorrect_verbose(self):
        argv = ["https://news.yahoo.com/rss/", "--verbose", "24"]
        with self.assertRaises(SystemExit):
            reader.main(argv)

    def test_uncorrect_date(self):
        argv = ["https://news.yahoo.com/rss/", "--date", "2001 09 11"]
        with self.assertRaises(SystemExit):
            reader.main(argv)

    def test_uncorrect_date_year(self):
        argv = ["https://news.yahoo.com/rss/", "--date", "20010911"]
        with self.assertRaises(SystemExit):
            self.assertRaises(ValueError, reader.main(argv))

    def test_verbose_file_handler(self):
        argv = ["https://news.yahoo.com/rss/", "--limit=5", "--verbose"]
        logger = app_logger.get_logger(__name__)
        self.assertTrue(logger.handlers[0].level == logging.INFO)

    def test_stream_handler(self):
        argv = ["https://news.yahoo.com/rss/", "--limit=5", "--verbose"]
        logger = app_logger.get_logger(__name__)
        self.assertTrue(logger.handlers[1].level == logging.ERROR)

    def test_verbose_stream_handler(self):
        argv = ["https://news.yahoo.com/rss/", "--limit=5", "--verbose"]
        reader.main()
        logger = app_logger.get_logger(__name__)
        self.assertTrue(logger.handlers[0].level == logging.INFO)
