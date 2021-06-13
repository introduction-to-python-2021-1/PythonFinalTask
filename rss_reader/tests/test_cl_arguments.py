import io
import sys
import unittest

from rss_reader import reader


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
