import io
import unittest
import rss_reader as RR
import sys


class TestProcessResponse(unittest.TestCase):

        def setUp(self):
            self.out = io.StringIO()
            sys.stdout = self.out

        def test_limit(self):
            parser = RR.create_parser(["--limit 5"])
            self.assertTrue(parser)

        def test_url(self):
            parser = RR.create_parser(["https://news.yahoo.com/rss/"])
            self.assertTrue(RR.open_url(parser.url))

        def test_version_none_argyment(self):

            with self.assertRaises(SystemExit):
                parser = RR.create_parser([None, "--version"])

            self.assertEqual(self.out.getvalue(), "Version 2.0\n")

        def test_json(self):
            parser = RR.create_parser(["https://news.yahoo.com/rss/", "--json"])
            self.assertTrue(parser.json)

        def test_verbose(self):
            parser = RR.create_parser(["https://news.yahoo.com/rss/", "--verbose"])
            self.assertTrue(parser.verbose)




if __name__ == "__main__":
    unittest.main()