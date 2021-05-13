import unittest
from unittest.mock import patch
from urllib.error import URLError

# import nose
from rss_reader import rss_reader as rs

NEWSLINK = "https://news.yahoo.com/rss/"


class MainReaderTests(unittest.TestCase):
    """
    Tests for Iteration I - main reader functionality
    """

    def test_bad_link(self):
        # Test if we give a bad link - Assertion is raising
        bad_link = "https://news.yaom/rss/"
        with self.assertRaises(URLError):
            rs.open_rss_link(bad_link, json=None, verbose=None, limit=None)

    @patch("builtins.print", autospec=True, side_effect=print)
    def test_json_news(self, mock_print):
        # Test output have the first key of our json dictionary ("news"), which is not present in the regular output
        rs.open_rss_link(NEWSLINK, json=True, verbose=None, limit=1)
        first_new = mock_print.call_args_list[0].args[0]
        self.assertTrue("news" in first_new)

    @patch("builtins.print", autospec=True, side_effect=print)
    def test_limit_really_limit(self, mock_print):
        # Test number of output lines is equal == limit * 5 (number of lines in one news WITHOUT logs no json)
        limit = 3
        rs.open_rss_link(NEWSLINK, json=None, verbose=None, limit=limit)
        news = mock_print.call_args_list
        self.assertEqual(len(news), limit * 5)


if __name__ == "__main__":
    unittest.main()
    # nose.run()
