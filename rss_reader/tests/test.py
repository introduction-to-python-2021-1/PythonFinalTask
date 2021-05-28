import unittest
from rss_reader.rss_reader import rss_reader
import io
import logging
import logging.handlers
import sys


class TestReader(unittest.TestCase):
    def test_checking_the_installation(self):
        """Creates object and outputs it to stdout"""
        self.output = io.StringIO()
        sys.stdout = self.output

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
        self.assertTrue(parser)

    def test_checking_verbose(self):
        """Test verbose status message"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertTrue(parser.verbose)

    def test_checking_verbose_plus(self):
        """Test verbose status message"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertLogs(parser, "Getting access to the RSS")

    def test_checking_verbose_plus1(self):
        """Test verbose status message"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        data = rss_reader.parses_data(parser, "--limit 1")
        self.assertLogs(data, "Reads amount of news - 1")

    def test_checking_verbose_plus_limit(self):
        """Test verbose status message and limit"""
        parser = rss_reader.command_arguments_parser(["--limit 7", "--verbose"])
        self.assertTrue(parser.verbose)

    def test_checking_json_format(self):
        """Test json format"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(parser.json)

    def test_checking_empty(self):
        """Test without link"""
        parser = rss_reader.command_arguments_parser([""])
        self.assertTrue(parser)

    def test_logging_INFO(self):
        """Test verbose"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertLogs(parser, logging.INFO)

    def test_logging_ERROR(self):
        """Test without verbose"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/"])
        self.assertLogs(parser, logging.ERROR)

    def test_answer_Exception(self):
        """Test answer for wrong URL"""
        answer = rss_reader.answer_URL(["https://news.sahoo.com/rss/"])
        self.assertLogs(answer, "Xml was failed. Input the correct URL, please")

    def test_bad_link_message(self):
        """Test Exception is raising and user-friendly message is printing to stdout, if we give a bad link"""
        parser = rss_reader.parses_data("https://news.sahoo.com/rss/", "--limit 1")
        with self.assertRaises(Exception):
            self.assertEqual(parser, "Xml was failed")

    def test_good_link(self):
        """Test for parser data with good link"""
        with open("../rss_reader/sources/yahoo_news.xml", "r") as rssfile:
            answer = rss_reader.parses_data(rssfile, "--limit 1")
            self.assertTrue(answer['feed'], "Yahoo News - Latest News & Headlines")

    def test_good_link_dict(self):
        """Test for dictionary with good link"""
        with open("../rss_reader/sources/yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
        self.assertEqual(len(rss_reader.parses_data(answer, 0)["news"]), 2)

    def test_good_link_for_dictionary_part(self):
        """Test for part in dictionary with good link"""
        with open("../rss_reader/sources/yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
        self.assertEqual(rss_reader.parses_data(answer, 0)["news"][1]["title"], "Big cheese no more: UK drug "
                                                                                "dealer caught out by cheese pic")
        self.assertEqual(rss_reader.parses_data(answer, 0)["news"][1]["link"], "https://news.yahoo.com/big-cheese"
                                                                               "-no-more-uk-112645101.html")
        self.assertEqual(rss_reader.parses_data(answer, 0)["news"][1]["pubDate"], "2021-05-27T11:26:45Z")
        self.assertIsInstance(rss_reader.parses_data(answer, 0), dict)
        print(len(rss_reader.parses_data(answer, 0)))
        self.assertEqual(len(rss_reader.parses_data(answer, 0)), 2)

    def test_good_link_in_json(self):
        """Test for dictionary in json"""
        with open("../rss_reader/sources/file_json_format.json", "r") as rssfile:
            answer = rssfile.read()
        self.assertIsInstance(rss_reader.parses_data(answer, 0), dict)

    def test_for_printing_news(self):
        """Test for def printing_news"""
        with open("../rss_reader/sources/yahoo_news.xml", "r") as rssfile:
            answer = rssfile.read()
            dictionary = rss_reader.parses_data(answer, 0)
            news = rss_reader.printing_news(dictionary)
        self.assertLogs(news, "https://s.yimg.com/uu/api/res/1.2/QWIOjpHY_PnmbmE8juiviQ--~B/aD0zOTEyO3c9NTM4NzthcHBp"
                              "ZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/ed73fe1143664266ccc00d223d7f84c2")


if __name__ == "__main__":
    unittest.main()
