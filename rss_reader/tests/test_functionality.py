import io
import json
import logging
import sys
import unittest
import urllib.error
import xml.etree.ElementTree
from pathlib import Path
from unittest import mock

import ddt
import validators

from rss_reader.rss_reader import rss_reader

VERSION = "2.0"

TESTS_DIR = Path(__file__).resolve().parent
XML = TESTS_DIR / "text.xml"
BAD_XML = TESTS_DIR / "bad.xml"

verbose_url_joint = mock.MagicMock()
verbose_url_joint.iter.return_value.__iter__.return_value = iter(
    ["https://news.yahoo.com/rss/", "--verbose"]
)
verbose_url_joint = list(verbose_url_joint.iter())

news_mock = mock.MagicMock()
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

wrong_news_mock = mock.MagicMock()
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


def mocked_urlopen(*args, **kwargs):
    """This function replaces behaviour of validation URL"""

    if not validators.url(args[0]):
        raise urllib.error.URLError("Incorrect URL")


@ddt.ddt
class TestParserArguments(unittest.TestCase):
    """This class tests parser arguments"""

    def setUp(self):
        """This method redirects stdout"""
        self.output = io.StringIO()
        sys.stdout = self.output

    def test_version(self):
        """Tests printing version with indicated --version argument"""
        with self.assertRaises(SystemExit):
            rss_reader.build_args([None, "--version"])
        self.assertEqual(self.output.getvalue(), f"Version {VERSION}\n")

    def test_version_with_url(self):
        """Tests printing version with indicated --version and source arguments"""
        with self.assertRaises(SystemExit):
            rss_reader.build_args(["https://news.yahoo.com/rss/", "--version"])
        self.assertEqual(self.output.getvalue(), f"Version {VERSION}\n")

    def test_verbose(self):
        """Tests if --verbose argument is True"""
        rss_parser = rss_reader.build_args(verbose_url_joint)
        self.assertTrue(rss_parser.verbose)

    def test_verbose_process(self):
        """Tests logging with indicated --verbose and source arguments"""
        rss_parser = rss_reader.build_args(verbose_url_joint)
        self.assertLogs(rss_parser, logging.INFO)

    def test_json(self):
        """Tests if --json argument is True"""
        rss_parser = rss_reader.build_args(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(rss_parser.json)

    @ddt.data("", "https://newssdasd2213.yahoo.com/rss/")
    def test_incorrect_url(self, url):
        """Tests logging if url is incorrect"""
        rss_parser = rss_reader.build_args(url)
        self.assertLogs(rss_parser, logging.ERROR)

    def test_limit(self):
        """Tests if --limit argument is True"""
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

    @mock.patch(
        "rss_reader.rss_reader.rss_reader.urllib.request.urlopen",
        side_effect=mocked_urlopen,
    )
    def test_response(self, mocked):
        """Tests exceptions connected with getting response from the specified source"""
        with self.assertRaises(SystemExit):
            with self.assertRaises(urllib.error.URLError):
                rss_reader.get_response("httpso://news.yahoo.com/rss/")
        with self.assertRaises(SystemExit):
            with self.assertRaises(ValueError):
                rss_reader.get_response("1313123131")


class TestParsing(unittest.TestCase):
    """This class tests parsing functionality"""

    def test_parse_response(self):
        news = rss_reader.parse_response(XML)
        self.assertEqual(news, news_mock)

    def test_parse_bad_response(self):
        with self.assertRaises(SystemExit):
            with self.assertRaises(xml.etree.ElementTree.ParseError):
                rss_reader.parse_response(BAD_XML)


class TestPrintingNews(unittest.TestCase):
    """Class tests printing functionality: custom and json"""

    def setUp(self):
        """This method redirects stdout"""
        self.output = io.StringIO()
        sys.stdout = self.output

    def test_custom_print(self):
        """This method tests custom print"""
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
        """This method tests printing news in json format"""
        limit = 1
        rss_reader.print_json(news_mock, limit)
        test_output = "".join(
            [
                '[\n  {\n    "Feed": "Yahoo News - Latest News & Headlines",\n',
                '    "Title": "Body of missing man found inside dinosaur statue",\n',
                '    "Date": "2021-05-24T15:35:42Z",\n',
                '    "Link": "https://news.yahoo.com/body-missing-man-found-inside-153542409.html"\n',
                "  }\n]\n",
            ]
        )
        self.assertEqual(self.output.getvalue(), test_output)

    def test_is_valid_json(self):
        """This method tests if printed json is valid"""
        limit = 1
        rss_reader.print_json(news_mock, limit)
        try:
            json.loads(self.output.getvalue())
        except json.JSONDecodeError:
            self.fail("JSONDecodeError")


if __name__ == "__main__":
    unittest.main()
