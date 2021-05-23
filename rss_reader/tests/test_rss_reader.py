import os
import io
import sys
import json
import unittest
from urllib.request import urlopen
from urllib.request import pathname2url

import ddt

from rss_reader.helper import VERSION
from rss_reader.rss_reader import main
from rss_reader.rss_reader import logger
from rss_reader.rss_reader import print_news
from rss_reader.rss_reader import get_response
from rss_reader.rss_reader import parse_response
from rss_reader.rss_reader import limit_news_items


class TestMain(unittest.TestCase):
    """Tests main function from rss_reader with various arguments."""

    def setUp(self):
        """Creates StringIO object and redirects stdout."""
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def test_url_and_version_arguments(self):
        """Tests that app prints its version and stops if URL and --version arguments are specified."""
        with self.assertRaises(SystemExit):
            main([None, "https://news.yahoo.com/rss/", "--version"])

        self.assertEqual(self.captured_output.getvalue(), f'"Version {VERSION}"\n')

    def test_just_version_argument(self):
        """Tests that app prints its version and stops if just --version argument is specified."""
        with self.assertRaises(SystemExit):
            main([None, "--version"])

        self.assertEqual(self.captured_output.getvalue(), f'"Version {VERSION}"\n')

    def tearDown(self):
        """Resets redirect of stdout."""
        sys.stdout = sys.__stdout__


class TestGetResponse(unittest.TestCase):
    """Tests get_response function from rss_reader."""

    def test_get_response_with_good_status_code(self):
        """Tests that get_response successfully gets response from server."""
        url = "https://www.google.com/"
        self.assertEqual(get_response(url).code, 200, "Wrong output size")


@ddt.ddt
class TestLimitNewsItems(unittest.TestCase):
    """Tests limit_news_items function from rss_reader with limit set to various values."""

    @ddt.data((None, 9), (-1, 0), (0, 0), (1, 1), (9, 9), (10, 9))
    @ddt.unpack
    def test_limit_news_items(self, limit, expected):
        """Tests set_limit function from rss_reader with limit set to various values."""
        with open("../rss_reader/project_data/json/news.json") as json_file:
            news_items = json.load(json_file)

        self.assertEqual(len(limit_news_items(news_items, limit)), expected, "Wrong output size")


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
        print_news(test_list)
        self.assertEqual(captured_output.getvalue(), test_output)
        # Resets redirect of stdout
        sys.stdout = sys.__stdout__


@ddt.ddt
class TestExceptions(unittest.TestCase):
    """Tests that get_response and parse_response functions from rss_reader handle exceptions."""

    @ddt.file_data("../project_data/json/testexceptionsdata.json")
    def test_get_response(self, url, expected):
        """Tests that get_response function handles exceptions."""
        with self.assertLogs(logger, "ERROR") as captured:
            with self.assertRaises(SystemExit):
                get_response(url)

            self.assertEqual(expected, captured.records[0].getMessage(), "Wrong output message")

    def test_parse_bad_response(self):
        """Tests that process_response function handles response with wrong xml structure."""
        fake_response = urlopen("file:" + pathname2url(os.path.abspath("project_data/xml/badsample.xml")))

        with self.assertLogs(logger, "ERROR") as captured:
            with self.assertRaises(SystemExit):
                parse_response(fake_response)

            self.assertEqual("Couldn't parse response", captured.records[0].getMessage())

        fake_response.close()


if __name__ == "__main__":
    unittest.main()
