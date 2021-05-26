import os
import io
import sys
import json
import unittest
from unittest.mock import patch, Mock
from urllib.error import URLError
from urllib.error import HTTPError

import ddt

from rss_reader import rss_reader
from rss_reader.helper import VERSION


class TestMain(unittest.TestCase):
    """Tests main function from rss_reader with various arguments."""

    def setUp(self):
        """Creates StringIO object and redirects stdout."""
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def test_url_and_version_arguments(self):
        """Tests that app prints its version and stops if URL and --version arguments are specified."""
        with self.assertRaises(SystemExit):
            rss_reader.main([None, "https://news.yahoo.com/rss/", "--version"])

        self.assertEqual(self.captured_output.getvalue(), f'"Version {VERSION}"\n')

    def test_just_version_argument(self):
        """Tests that app prints its version and stops if just --version argument is specified."""
        with self.assertRaises(SystemExit):
            rss_reader.main([None, "--version"])

        self.assertEqual(self.captured_output.getvalue(), f'"Version {VERSION}"\n')

    def tearDown(self):
        """Resets redirect of stdout."""
        sys.stdout = sys.__stdout__


@ddt.ddt
@patch.object(rss_reader, "urlopen")
class TestGetResponse(unittest.TestCase):
    """Tests get_response function from rss_reader."""

    def test_get_response_with_valid_url(self, mocked):
        """Tests that get_response function from rss_reader closes connection after successful response from server."""
        mocked.return_value = response_mock = Mock()
        rss_reader.get_response("https://news.yahoo.com/rss/")
        response_mock.close.assert_called()

    @ddt.file_data("../project_data/json/test_get_response.json")
    def test_get_response_with_exceptions(self, mocked, string_with_exception_creation, exception_attributes, message):
        """Tests that get_response function from rss_reader handles various exceptions."""
        mocked.side_effect = eval(string_with_exception_creation, globals(), exception_attributes)

        with self.assertLogs(rss_reader.logger, "ERROR") as captured:
            with self.assertRaises(SystemExit):
                rss_reader.get_response("")

            self.assertEqual(message.format(**exception_attributes), captured.records[0].getMessage())


class TestParseResponse(unittest.TestCase):
    """Tests parse_response function from rss_reader."""

    def test_parse_response_with_bad_xml(self):
        """Tests that parse_response function from rss_reader raises exception when tag rss ins't in xml structure."""
        with self.assertLogs(rss_reader.logger, "ERROR") as captured:
            with self.assertRaises(SystemExit):
                rss_reader.parse_response(b"<channel></channel>")

            self.assertEqual("Couldn't parse response: the document isn't RSS feed", captured.records[0].getMessage())


@ddt.ddt
class TestLimitNewsItems(unittest.TestCase):
    """Tests limit_news_items function from rss_reader with limit set to various values."""

    @ddt.data((None, 9), (-1, 0), (0, 0), (1, 1), (9, 9), (10, 9))
    @ddt.unpack
    def test_limit_news_items(self, limit, expected):
        """Tests set_limit function from rss_reader with limit set to various values."""
        with open("../rss_reader/project_data/json/news.json") as json_file:
            news_items = json.load(json_file)

        self.assertEqual(len(rss_reader.limit_news_items(news_items, limit)), expected, "Wrong output size")


class TestPrintNews(unittest.TestCase):
    """Tests print_news fucntion from rss_reader."""

    def test_print_news(self):
        """Tests that print_news properly prints list with news items."""
        # Create data for testing
        test_list = [
            {
                "Feed": "TUT.BY: Новости Витебска и Витебской области",
                "Title": "В Орше взорвали старое здание одного из предприятий",
                "Date": "Mon, 10 May 2021 12:52:00 +0300",
                "Link": "https://news.tut.by/culture/"
            }
        ]
        test_output = "".join((
            "\nFeed: TUT.BY: Новости Витебска и Витебской области\n",
            "Title: В Орше взорвали старое здание одного из предприятий\n",
            "Date: Mon, 10 May 2021 12:52:00 +0300\n",
            "Link: https://news.tut.by/culture/\n"
        ))
        # Create StringIO object and redirects stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        # Perform testing
        rss_reader.print_news(test_list)
        self.assertEqual(captured_output.getvalue(), test_output)
        # Resets redirect of stdout
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
