"""The main test module for basic rss feed reading"""
import unittest
from rss_reader.rss_reader import rss_reader
import logging
import logging.handlers
from unittest.mock import patch
from rss_reader.rss_reader import test_data
from datetime import datetime
import os
import json


class TestReader(unittest.TestCase):
    """Tests for parsing links, making news dictionaries, printing news, setting limits, verbose flag"""

    def test_set_limit_for_print(self):
        """Good limit"""
        parser = rss_reader.command_arguments_parser(["--limit 3"])
        self.assertTrue(parser)

    def test_0_limit(self):
        """Test limit zero"""
        parser = rss_reader.command_arguments_parser(["--limit 0"])
        self.assertTrue(parser)

    def test_0_limit_message(self):
        """Test limit zero message"""
        parser = rss_reader.command_arguments_parser(["--limit 0"])
        self.assertLogs(parser, "Invalid limit. Enter the limit (greater than 0), please")

    def test_limit_negative_number(self):
        """Test limit negative number"""
        parser = rss_reader.command_arguments_parser(["--limit -5"])
        self.assertLogs(parser, "Invalid limit. Enter the limit (greater than 0), please")

    def test_checking_verbose(self):
        """Test verbose status message"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertTrue(parser.verbose)
        self.assertLogs(parser, "Getting access to the RSS")
        self.assertLogs(parser, "Starting reading link https://news.yahoo.com/rss/")

    def test_checking_json_format(self):
        """Test json format"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(parser.json)

    def test_checking_empty(self):
        """Test without link"""
        parser = rss_reader.command_arguments_parser([""])
        self.assertTrue(parser)
        self.assertLogs(parser, "Incorrect URL. This is not the rss feed address")

    def test_checking_wrong(self):
        """Test wrong link"""
        parser = rss_reader.command_arguments_parser(["ghhkkk"])
        self.assertTrue(parser)
        self.assertLogs(parser, "Insert rss link, please")
        self.assertTrue(parser, "Incorrect URL. This is not the rss feed address")

    def test_checking_wrong_url(self):
        """Test wrong link"""
        parser = rss_reader.command_arguments_parser(["https://news.sahoo.com/rss/"])
        self.assertTrue(parser)
        self.assertLogs(parser, "ConnectionError, try again, please")

    def test_checking_url(self):
        """Test wrong link"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rs/"])
        self.assertTrue(parser, "Error 404. Please try to reload the page or check the link you entered")

    def test_logging_INFO(self):
        """Test verbose"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertLogs(parser, logging.INFO)

    def test_logging_ERROR(self):
        """Test without verbose"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/"])
        self.assertLogs(parser, logging.ERROR)

    def test_bad_link_message(self):
        """Test Exception is raising and user-friendly message is printing to stdout, if we give a bad link"""
        parser = rss_reader.parses_data("https://news.sahoo.com/rss/", source=None)
        with self.assertRaises(Exception):
            self.assertEqual(parser, "Xml was failed")

    def test_good_link(self):
        """Test for parser data with good link"""
        with open("yahoo_news.xml", "r") as rssfile:
            answer = rss_reader.parses_data(rssfile, source=None)
            self.assertTrue(answer["feed"], "Yahoo News - Latest News & Headlines")

    def test_good_link_data(self):
        """Test for data with good link"""
        with open("yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
        self.assertEqual(len(rss_reader.parses_data(answer, source=None)["news"]), 2)

    def test_good_link_for_data_part(self):
        """Test for part in dictionary with good link"""
        with open("yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
        self.assertEqual(rss_reader.parses_data(answer, source=None)["news"][1]["title"], "Big cheese no more: UK drug"
                                                                                          "dealer caught out by cheese"
                                                                                          "pic")
        self.assertEqual(rss_reader.parses_data(answer, source=None)["news"][1]["link"], "https://news.yahoo.com/"
                                                                                         "big-cheese-no-more-uk-"
                                                                                         "112645101.html")
        self.assertEqual(rss_reader.parses_data(answer, source=None)["news"][1]["pubDate"], "2021-05-27T11:26:45Z")
        self.assertIsInstance(rss_reader.parses_data(answer, source=None), dict)
        self.assertLogs(rss_reader.parses_data(answer, source=None)["news"][1], "Reads amount of news - 1")


    def test_good_link_in_json(self):
        """Test for data in json"""
        with open("file_json_format.json", "r") as rssfile:
            answer = rssfile.read()
        self.assertIsInstance(rss_reader.parses_data(answer, source=None), dict)
        self.assertLogs(answer, "In json")

    def test_for_printing_news(self):
        """Test for def printing_news"""
        with open("yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
            data = rss_reader.parses_data(answer, source=None)
            news = rss_reader.printing_news(data, 1)
        self.assertLogs(news, "https://s.yimg.com/uu/api/res/1.2/QWIOjpHY_PnmbmE8juiviQ--~B/aD0zOTEyO3c9NTM4NzthcHBp"
                              "ZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/ed73fe1143664266ccc00d223d7f84c2")

    # Tests for function "printing_json"
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_printing_json(self, mock_print):
        """Test for output in json format"""
        rss_reader.printing_json(test_data.DATA_FOR_TEST, 1)
        first = mock_print.call_args_list[0].args[0]
        self.assertTrue("Title" in first)

    def test_for_logger(self):
        "Test for logs with verbose argument"
        logger = rss_reader.create_logger("verbose")
        self.assertTrue(logger, "%(asctime)s - %(levelname)s - %(message)s")
        self.assertTrue(logging.INFO, "Getting access to the RSS")

    def test_date_compare(self):
        """Provide comparison of dates"""
        user_date = datetime.strptime("20210607", '%Y%m%d')
        self.assertTrue(rss_reader.compare_dates("Sunday, 07 June 2021 00:35:00", user_date))

    def test_date_compare_incorrect(self):
        """Provide comparison of dates"""
        user_date = datetime.strptime("20210607", '%Y%m%d')
        self.assertFalse(rss_reader.compare_dates("Fri, 08 June 2021 11:15:18 -0400", user_date))

    def test_incorrect_date(self):
        """Test ValueError with incorrect number instead of a date"""
        with self.assertRaises(ValueError):
            rss_reader.creating_cashing_news_data("567899976")

    def test_news_cashing(self):
        """Test for cashing news"""
        rss_reader.news_cashing(test_data.DATA_FOR_TEST)
        cash_file = os.path.join(os.getcwd(), "cashing_news.txt")
        with open(cash_file, "r") as cash_file:
            lines = cash_file.readlines()
            last_line = lines[-1]
            data = json.loads(last_line)
            self.assertEqual(data, test_data.DATA_FOR_TEST)


if __name__ == "__main__":
    unittest.main()
