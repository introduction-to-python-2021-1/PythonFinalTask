import unittest
from rss_reader.rss_reader import rss_reader
import sys
import io

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
        self.assertLogs(parser, f"Getting access to the RSS")


    def test_checking_verbose_plus_limit(self):
        """Test verbose status message and limit"""
        parser = rss_reader.command_arguments_parser(["--limit 4", "--verbose"])
        self.assertTrue(parser.verbose)

    def test_checking_json_format(self):
        """Test json format"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(parser.json)

    def test_checking_empty(self):
        """Test without link"""
        parser = rss_reader.command_arguments_parser([""])
        self.assertTrue(parser)


if __name__ == "__main__":
    unittest.main()
