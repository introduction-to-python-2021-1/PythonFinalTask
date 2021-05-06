import io
import sys
import unittest

from rss_reader import main
from rss_reader import VERSION


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

        self.assertEqual(self.captured_output.getvalue(), '"Version 2.0"\n')

    def test_just_version_argument(self):
        """Tests that app prints its version and stops if just --version argument is specified."""
        with self.assertRaises(SystemExit):
            main([None, "--version"])

        self.assertEqual(self.captured_output.getvalue(), f'"Version {VERSION}"\n')

    def tearDown(self):
        """Resets redirect of stdout."""
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
