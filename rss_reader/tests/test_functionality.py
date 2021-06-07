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

VERSION = "3.0"

TESTS_DIR = Path(__file__).resolve().parent
XML = TESTS_DIR / "text.xml"
BAD_XML = TESTS_DIR / "bad.xml"

verbose_url_joint = mock.MagicMock()
verbose_url_joint.iter.return_value.__iter__.return_value = iter(
    [None, "https://news.yahoo.com/rss/", "--verbose"]
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
    response = mock.MagicMock(status_code=200, payload=json.dumps({"key": "payload"}))
    return response


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
            rss_reader.main([None, "--version"])
        self.assertEqual(self.output.getvalue(), f"Version {VERSION}\n")

    def test_version_with_url(self):
        """Tests printing version with indicated --version and source arguments"""
        with self.assertRaises(SystemExit):
            rss_reader.main([None, "https://news.yahoo.com/rss/", "--version"])
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
        rss_parser = rss_reader.build_args(
            [None, "https://news.yahoo.com/rss/", "--json"]
        )
        self.assertTrue(rss_parser.json)

    @ddt.data("", "https://newssdasd2213.yahoo.com/rss/")
    def test_incorrect_url(self, source):
        """Tests logging if url is incorrect"""
        rss_parser = rss_reader.build_args([None, source])
        self.assertLogs(rss_parser, logging.ERROR)

    @ddt.data(("https://news.yahoo.com/rss/", 1))
    @ddt.unpack
    def test_limit(self, source, limit):
        """Tests if --limit argument is True"""
        rss_parser = rss_reader.build_args([None, source, f"--limit={limit}"])
        self.assertTrue(rss_parser.limit)

    @ddt.data(-1, 0)
    def test_logging_with_incorrect_limit(self, limit):
        """Tests logging with incorrect limit"""
        with self.assertRaises(SystemExit):
            rss_parser = rss_reader.main(
                [None, "https://news.yahoo.com/rss/", f"--limit={limit}"]
            )
            self.assertLogs(rss_parser, logging.ERROR)

    @ddt.data(1, 23)
    def test_limit_performance(self, limit):
        news_list = rss_reader.parse_response(XML)
        limit_news_list = rss_reader.calculate_news_with_limit(news_list, limit)
        self.assertEqual(len(limit_news_list), 1)

    @ddt.data(
        ("httpso://news.yahoo.com/rss/", urllib.error.URLError),
        ("1313123131", ValueError),
    )
    @ddt.unpack
    @mock.patch(
        "rss_reader.rss_reader.rss_reader.urllib.request.urlopen",
        side_effect=mocked_urlopen,
    )
    def test_response_with_bad_source(self, source, error, mocked):
        """Tests exceptions connected with getting response from the specified source"""
        with self.assertRaises(SystemExit):
            with self.assertRaises(error):
                rss_reader.get_response(source)

    @mock.patch(
        "rss_reader.rss_reader.rss_reader.urllib.request.urlopen",
        side_effect=mocked_urlopen,
    )
    def test_response_with_good_source(self, mocked):
        """Tests response with good source"""
        response = rss_reader.get_response("https://news.yahoo.com/rss/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.payload, json.dumps({"key": "payload"}))


class TestParsing(unittest.TestCase):
    """This class tests parsing functionality"""

    def test_parse_response(self):
        """This method tests parsing good xml and compares news list after parsing"""
        news_list = rss_reader.parse_response(XML)
        self.assertEqual(news_list, news_mock)

    def test_parse_bad_response(self):
        """This method tests parsing bad xml: raising ParseError"""
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
        rss_reader.print_news(news_mock)
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
        rss_reader.print_json(news_mock)
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
        rss_reader.print_json(news_mock)
        try:
            json.loads(self.output.getvalue())
        except json.JSONDecodeError:
            self.fail("JSONDecodeError")


if __name__ == "__main__":
    unittest.main()
