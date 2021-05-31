"""The main test module for basic rss feed reading"""
import unittest
from rss_reader.rss_reader import rss_reader
import logging
import logging.handlers
from unittest.mock import patch
import test_data


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

    def test_checking_json_format(self):
        """Test json format"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(parser.json)

    def test_checking_empty(self):
        """Test without link"""
        parser = rss_reader.command_arguments_parser([""])
        self.assertTrue(parser)
        self.assertLogs(parser, "Insert rss link, please")

    def test_checking_wrong(self):
        """Test wrong link"""
        parser = rss_reader.command_arguments_parser(["ghhkkk"])
        self.assertTrue(parser)
        self.assertLogs(parser, "Insert rss link, please")

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
        parser = rss_reader.parses_data("https://news.sahoo.com/rss/")
        with self.assertRaises(Exception):
            self.assertEqual(parser, "Xml was failed")

    def test_good_link(self):
        """Test for parser data with good link"""
        with open("yahoo_news.xml", "r") as rssfile:
            answer = rss_reader.parses_data(rssfile)
            self.assertTrue(answer["feed"], "Yahoo News - Latest News & Headlines")

    def test_good_link_data(self):
        """Test for data with good link"""
        with open("yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
        self.assertEqual(len(rss_reader.parses_data(answer)["news"]), 2)

    def test_good_link_for_data_part(self):
        """Test for part in dictionary with good link"""
        with open("yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
        self.assertEqual(rss_reader.parses_data(answer)["news"][1]["title"], "Big cheese no more: UK drug "
                                                                             "dealer caught out by cheese pic")
        self.assertEqual(rss_reader.parses_data(answer)["news"][1]["link"], "https://news.yahoo.com/big-cheese"
                                                                            "-no-more-uk-112645101.html")
        self.assertEqual(rss_reader.parses_data(answer)["news"][1]["pubDate"], "2021-05-27T11:26:45Z")
        self.assertIsInstance(rss_reader.parses_data(answer), dict)
        self.assertLogs(rss_reader.parses_data(answer)["news"][1], "Reads amount of news - 1")
        self.assertLogs(answer, "Starting reading link")

    def test_good_link_in_json(self):
        """Test for data in json"""
        with open("file_json_format.json", "r") as rssfile:
            answer = rssfile.read()
        self.assertIsInstance(rss_reader.parses_data(answer), dict)
        self.assertLogs(answer, "In json")

    def test_for_printing_news(self):
        """Test for def printing_news"""
        with open("yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
            data = rss_reader.parses_data(answer)
            news = rss_reader.printing_news(data, 1)
        self.assertLogs(news, "https://s.yimg.com/uu/api/res/1.2/QWIOjpHY_PnmbmE8juiviQ--~B/aD0zOTEyO3c9NTM4NzthcHBp"
                              "ZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/ed73fe1143664266ccc00d223d7f84c2")

    # Tests for function "printing_json"
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_printing_json(self, mock_print):
        """ Test for output in json format"""
        rss_reader.printing_json(test_data.DATA_FOR_TEST, 1)
        first = mock_print.call_args_list[0].args[0]
        self.assertTrue("Title" in first)


if __name__ == "__main__":
    unittest.main()
