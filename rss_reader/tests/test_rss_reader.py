import io
import unittest
from urllib.error import URLError
from rss_reader import rss_reader
import sys


class TestProcessResponse(unittest.TestCase):
    def setUp(self):
        self.out = io.StringIO()
        sys.stdout = self.out

    def test_limit(self):
        """Test positive limit"""
        parser = rss_reader.create_parser(["--limit 5"])
        self.assertTrue(parser)

    def test_zero_limit(self):
        """Test zero limit"""
        parser = rss_reader.create_parser(["--limit 0"])
        self.assertTrue(parser)
 
    def test_bad_url(self):
        """Try test bad urs page"""
        parser = rss_reader.create_parser(["https://newsyahoo.com/rss/"])
        with self.assertRaises(SystemExit):
            with self.assertRaises(URLError):
                self.assertEqual(rss_reader.open_url(parser.url), f"cant open or found {parser.url}")
                
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

    def test_bad_date(self):
        """Test bad data"""
        parser = rss_reader.create_parser(["--date 20"])
        self.assertLogs(parser, "Bad date format")

    def test_word_date(self):
        """Test date word format"""
        parser = rss_reader.create_parser(["--date slovo"])
        self.assertLogs(parser, "Bad date format")


if __name__ == "__main__":
    unittest.main()
