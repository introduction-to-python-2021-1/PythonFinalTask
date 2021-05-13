import io
import unittest
from rss_reader import rss_reader
import sys


class TestProcessResponse(unittest.TestCase):
    def setUp(self):
        self.out = io.StringIO()
        sys.stdout = self.out

    def test_limit(self):
        parser = rss_reader.create_parser(["--limit 5"])
        self.assertTrue(parser)

    def test_url(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/"])
        self.assertTrue(rss_reader.open_url(parser.url))

    def test_version_none_argyment(self):
        with self.assertRaises(SystemExit):
            parser = rss_reader.create_parser([None, "--version"])

        self.assertEqual(self.out.getvalue(), "Version 2.0\n")

    def test_json(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(parser.json)

    def test_verbose(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertTrue(parser.verbose)


if __name__ == "__main__":
    unittest.main()
