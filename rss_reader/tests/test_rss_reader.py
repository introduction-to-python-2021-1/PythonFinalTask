import io
import os
import sys
import logging
import unittest
from urllib.error import URLError

import pandas as pd
from rss_reader import rss_reader
from rss_reader.dataset import Data


class TestArg(unittest.TestCase):
    def setUp(self):
        self.out = io.StringIO()
        sys.stdout = self.out


    def test_version_none_argyment(self):
        """Test version without url"""
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

    def test_verbose_(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertLogs(parser, f"open {parser.url} and start parse")


class TestException(unittest.TestCase):
    def test_printException(self):
        """Test not rss format"""
        with self.assertWarns(ResourceWarning):
            data = Data()
        parser = rss_reader.create_parser(["https://news.yahoo.com", "-l 1"])
        with self.assertRaises(SystemExit):
            self.assertLogs(rss_reader.parse_news(parser, data), logging.ERROR)

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
    def setUp(self):
        self.out = io.StringIO()
        sys.stdout = self.out

    def test_negative_limit(self):
        """Test negative limit"""
        parser = rss_reader.create_parser(["https://newsyahoo.com/rss/", "-l-1"])
        with self.assertRaises(SystemExit):
            rss_reader.limit_checker(parser)
            self.assertEqual(self.out.getvalue(),
                             f"The limit was entered incorrectly (You enter limit = {parser.limit}) ")

    def test_zero_limit(self):
        """Test zero limit"""
        parser = rss_reader.create_parser(["https://newsyahoo.com/rss/", "-l0"])
        with self.assertRaises(SystemExit):
            rss_reader.limit_checker(parser)
            self.assertEqual(self.out.getvalue(),
                             f"The limit was entered incorrectly (You enter limit = {parser.limit}) ")

    def test_normal_limit(self):
        """Test limit"""
        parser = rss_reader.create_parser(["https://newsyahoo.com/rss/", "-l1"])
        self.assertEqual(parser.limit, 1)

    def test_none_limit(self):
        """Test None limit"""
        parser = rss_reader.create_parser(["https://newsyahoo.com/rss/"])
        self.assertIsNone(parser.limit)


class TestDate(unittest.TestCase):
    def setUp(self):
        self.out = io.StringIO()
        sys.stdout = self.out

    def test_bad_date(self):
        """Test bad data"""
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "-d 20"])
        with self.assertRaises(SystemExit):
            with open("data.csv", "w"):
                rss_reader.date_checker(parser)
                self.assertEqual(self.out.getvalue(), "Bad date format")

    def test_word_date(self):
        """Test date word format"""
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "-d word"])
        with self.assertRaises(SystemExit):
            rss_reader.date_checker(parser)
            self.assertEqual(self.out.getvalue(), "Bad date format")

    def test_none_date(self):
        """Test empty date"""
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "-d "])
        with self.assertRaises(SystemExit):
            rss_reader.date_checker(parser)
            self.assertEqual(self.out.getvalue(), "Bad date format")


class TestPrint(unittest.TestCase):
    def setUp(self):
        self.out = io.StringIO()
        sys.stdout = self.out

    def test_print(self):
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/"])
        text = dict()
        text["Title"] = "Man charged with threatening to kill President Biden",
        text["Date"] = "2021-05-28T11:06:25Z",
        text["Link"] = "https://news.yahoo.com/man-charged-threatening-kill-president-110625146.html",
        text = pd.DataFrame(text)
        ans = """Title : Man charged with threatening to kill President Biden
Date : 2021-05-28T11:06:25Z
Link : https://news.yahoo.com/man-charged-threatening-kill-president-110625146.html\n\n"""
        rss_reader.print_news(parser, text)
        self.assertEqual(self.out.getvalue(), ans)

    def test_print_json(self):
        ans = """{
   "Title": "Gilbert Poole Jr: Man cleared of murder and set free after 32 years in prison",
   "Date": "2021-05-27T08:55:55Z",
   "Link": "https://news.yahoo.com/gilbert-poole-jr-man-cleared-085555782.html"
}
"""
        text = dict()
        text["Title"] = "Gilbert Poole Jr: Man cleared of murder and set free after 32 years in prison",
        text["Date"] = "2021-05-27T08:55:55Z",
        text["Link"] = "https://news.yahoo.com/gilbert-poole-jr-man-cleared-085555782.html"
        text = pd.DataFrame(text)
        parser = rss_reader.create_parser(["https://news.yahoo.com/rss/", "--json"])
        rss_reader.print_news(parser, text)
        self.assertEqual(self.out.getvalue(), ans)


if __name__ == "__main__":
    unittest.main()
