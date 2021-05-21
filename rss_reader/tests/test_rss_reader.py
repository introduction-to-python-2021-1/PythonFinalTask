import io
import logging
import unittest
from urllib.error import URLError
from rss_reader import rss_reader
import sys


class TestProcessResponse(unittest.TestCase):
    def setUp(self):
        self.out = io.StringIO()
        sys.stdout = self.out

    def test_version_none_argyment(self):
        """Test version with out url"""
        with self.assertRaises(SystemExit):
            parser = rss_reader.create_parser([None, "--version"])
        self.assertEqual(self.out.getvalue(), "Version 3.0\n")

    def test_version_url(self):
        """Test version with url"""
        with self.assertRaises(SystemExit):
            parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--version"])
        self.assertEqual(self.out.getvalue(), "Version 3.0\n")

    def test_empty(self):
        """Test empty line """
        parser = rss_reader.create_parser([""])
        self.assertTrue(parser)

    def test_json(self):
        """Test JSON output"""
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(parser.json)

    def test_verbose(self):
        """Test log"""
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertTrue(parser.verbose)

    def test_date(self):
        """Test date"""
        parser = rss_reader.create_parser(["--date 20210521"])
        self.assertTrue(parser)

    def test_verbose_(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertLogs(parser, f"open {parser.url} and start parse")


class TestMain(unittest.TestCase):
    def test_log(self):
        """Test verbose on main"""
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertLogs(parser, logging.INFO)

    def test_lvl_log(self):
        """Test lvl log without verbose"""
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/"])
        self.assertLogs(parser, logging.ERROR)

    def test_bad_date(self):
        """Test bad data"""
        parser = rss_reader.create_parser(["--date 20"])
        self.assertLogs(parser, "Bad date format")

    def test_word_date(self):
        """Test date word format"""
        parser = rss_reader.create_parser(["--date word"])
        self.assertLogs(parser, "Bad date format")


class TestException(unittest.TestCase):
    def test_printException(self):
        """Test not rss format"""
        parser = rss_reader.create_parser(["https://news.yahoo.com", "-l 1"])
        with self.assertRaises(SystemExit):
            self.assertLogs(rss_reader.print_news(parser), logging.ERROR)

    def test_bad_url(self):
        """Try test bad urs page"""
        parser = rss_reader.create_parser(["https://newsyahoo.com/rss/"])
        with self.assertRaises(SystemExit):
            with self.assertRaises(URLError):
                self.assertEqual(rss_reader.open_url(parser.url), f"cant open or found {parser.url}")

    def test_url(self):
        """Test normal Url"""

        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/"])
        self.assertTrue(rss_reader.open_url(parser.url))


class TestLimit(unittest.TestCase):
    def test_zero_limit(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "-l0"])
        self.assertFalse(parser.limit)

    def test_negative_limit(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "-l-1"])
        with self.assertRaises(SystemExit):
            self.assertLogs(rss_reader.print_news(parser), logging.ERROR)

    def test_normal_limit(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "-l 1"])
        self.assertTrue(parser.limit)

if __name__ == "__main__":
    unittest.main()
