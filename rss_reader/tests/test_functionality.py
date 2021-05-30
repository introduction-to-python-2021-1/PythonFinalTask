import io
import logging
import sys
import unittest
import urllib.error
import xml.etree.ElementTree
from pathlib import Path

from rss_reader import rss_reader
from unittest.mock import MagicMock
import json

VERSION = "1.0"

TESTS_DIR = Path(__file__).resolve().parent
XML = TESTS_DIR / "text.xml"
BAD_XML = TESTS_DIR / "bad.xml"

verbose_url_joint = MagicMock()
verbose_url_joint.iter.return_value.__iter__.return_value = iter(
    ["https://news.yahoo.com/rss/", "--verbose"]
)
verbose_url_joint = list(verbose_url_joint.iter())

news_mock = MagicMock()
news_mock.iter.return_value.__iter__.return_value = iter(
    [
        {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Body of missing man found inside dinosaur statue",
            "Date": "2021-05-24T15:35:42Z",
            "Link": "https://news.yahoo.com/body-missing-man-found-inside-153542409.html",
        }
    ]
)
news_mock = list(news_mock.iter())

wrong_news_mock = MagicMock()
wrong_news_mock.iter.return_value.__iter__.return_value = iter(
    [
        {
            "Fddd": "Yahoo News - Latest News & Headlines",
            "Title": "Body of missing man found inside dinosaur statue",
            "Date": "2021-05-24T15:35:42Z",
            "Link": "https://news.yahoo.com/body-missing-man-found-inside-153542409.html",
        }
    ]
)
wrong_news_mock = list(wrong_news_mock.iter())


class TestParserArguments(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        sys.stdout = self.output

    def test_version(self):
        with self.assertRaises(SystemExit):
            rss_parser = rss_reader.build_args([None, "--version"])
        self.assertEqual(self.output.getvalue(), f"Version {VERSION}\n")

    def test_version_with_url(self):
        with self.assertRaises(SystemExit):
            rss_reader.build_args(["https://news.yahoo.com/rss/", "--version"])
        self.assertEqual(self.output.getvalue(), f"Version {VERSION}\n")

    def test_verbose(self):
        rss_parser = rss_reader.build_args(verbose_url_joint)
        self.assertTrue(rss_parser.verbose)

    def test_verbose_process(self):
        rss_parser = rss_reader.build_args(verbose_url_joint)
        self.assertLogs(rss_parser, logging.INFO)

    def test_json(self):
        rss_parser = rss_reader.build_args(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(rss_parser.json)

    def test_incorrect_url(self):
        rss_parser = rss_reader.build_args([""])
        self.assertLogs(rss_parser, logging.ERROR)
        rss_parser = rss_reader.build_args(["https://newssdasd2213.yahoo.com/rss/"])
        self.assertLogs(rss_parser, logging.ERROR)

    def test_limit(self):
        rss_parser = rss_reader.build_args(["https://news.yahoo.com/rss/", "--limit=1"])
        self.assertTrue(rss_parser.limit)

    def test_incorrect_limit_0(self):
        rss_parser = rss_reader.build_args(["https://news.yahoo.com/rss/", "--limit=0"])
        self.assertLogs(rss_parser, logging.ERROR)

    def test_incorrect_limit_negative(self):
        rss_parser = rss_reader.build_args(
            ["https://news.yahoo.com/rss/", "--limit=-1"]
        )
        self.assertLogs(rss_parser, logging.ERROR)


class TestParsing(unittest.TestCase):
    def test_parse_response(self):
        news = rss_reader.parse_response(XML)
        self.assertEqual(news, news_mock)

    def test_parse_bad_response(self):
        with self.assertRaises(SystemExit):
            with self.assertRaises(xml.etree.ElementTree.ParseError):
                rss_reader.parse_response(BAD_XML)


class TestPrintingNews(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        sys.stdout = self.output

    def test_custom_print(self):
        limit = 1
        rss_reader.print_news(news_mock, limit)
        test_output = "".join(
            [
                "Feed: Yahoo News - Latest News & Headlines\n",
                "Title: Body of missing man found inside dinosaur statue\n",
                "Date: 2021-05-24T15:35:42Z\n",
                "Link: https://news.yahoo.com/body-missing-man-found-inside-153542409.html\n",
                "....................\n",
            ]
        )
        self.assertEqual(self.output.getvalue(), test_output)

    def test_json_print(self):
        limit = 1
        rss_reader.print_json(news_mock, limit)
        try:
            json.loads(self.output.getvalue())
        except json.JSONDecodeError:
            self.fail("JSONDecodeError")


class TestRaisingExceptions(unittest.TestCase):
    def test_response(self):
        with self.assertRaises(SystemExit):
            with self.assertRaises(urllib.error.URLError):
                rss_reader.get_response("https://newssdasd2213.yahoo.com/rss/")
        with self.assertRaises(SystemExit):
            with self.assertRaises(ValueError):
                rss_reader.get_response("1313123131")


if __name__ == "__main__":
    unittest.main()
