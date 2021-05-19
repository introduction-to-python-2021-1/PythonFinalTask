import unittest
from unittest import mock
from unittest.mock import patch

import feedparser
import test_data as td
from rss_reader import rss_reader as rs

NEWSLINK = "https://news.yahoo.com/rss/"


class TestMainReader(unittest.TestCase):
    """
    Tests for effective parsing links, printing news in json and normal format,
    setting and working limits of the numbers of news.
    """

    #  Tests for function "open_rss_link"
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_bad_link(self, mock_print):
        # Test URLError is raising and user-friendly message is printing to stdout, if we give a bad link
        bad_link = "https://news.yaom/rss/"
        rs.open_rss_link(bad_link, verbose=None)
        message = mock_print.call_args_list[0].args[0]
        self.assertEqual(message, "Bad link, please try again")

    @patch("builtins.print", autospec=True, side_effect=print)
    def test_no_link(self, mock_print):
        # Test ValueError is raising and user-friendly message is printing to stdout, if we give a bad link
        rs.open_rss_link("", verbose=None)
        message = mock_print.call_args_list[0].args[0]
        self.assertEqual(message, "Please insert rss link")

    def test_normal_link(self):
        # Test parsing of the normal ling Yahoo NEWSLINK goes good and we receive expected header
        content = rs.open_rss_link(NEWSLINK, verbose=None)
        self.assertEqual(content.feed.title, "Yahoo News - Latest News & Headlines")

    # Tests for function "printing_parsing_news"
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_normal_print(self, mock_print):
        # Test we have first row as expected
        content = feedparser.parse(NEWSLINK)
        rs.printing_parsing_news(content, 1)
        message_head = mock_print.call_args_list[0].args[0]
        self.assertEqual(message_head, "\nYahoo News - Latest News & Headlines\n")

    @patch("builtins.print", autospec=True, side_effect=print)
    def test_limit_really_limit_one(self, mock_print):
        # Test number of output lines is equal limit * 5 (number of lines in one news WITHOUT logs no json)
        content = mock.MagicMock()
        content.entries = td.TEST_ENTRIES
        rs.printing_parsing_news(content, 1)
        news = mock_print.call_args_list
        self.assertEqual(len(news), (1 * 5) + 1)

    @patch("builtins.print", autospec=True, side_effect=print)
    def test_limit_really_three(self, mock_print):
        # Test number of output lines is equal limit * 5 (number of lines in one news WITHOUT logs no json)
        content = mock.MagicMock()
        content.entries = td.TEST_ENTRIES
        rs.printing_parsing_news(content, 3)
        news = mock_print.call_args_list
        self.assertEqual(len(news), (3 * 5) + 1)

    # Tests for function "printing_parsing_news_in_json"
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_printing_parsing_news_in_json(self, mock_print):
        # Test output have the first key of our json dictionary ("news"), which is not present in the regular output
        content = mock.MagicMock()
        content.entries = td.TEST_ENTRIES
        rs.printing_parsing_news_in_json(content, 1)
        first_new = mock_print.call_args_list[0].args[0]
        self.assertTrue("news" in first_new)

    # Tests for function "set_limit"
    def test_limit_is_not_passed(self):
        # Test case user do not pass any limit
        content = mock.MagicMock()
        content.entries = td.TEST_ENTRIES
        limit = None
        number_of_news_to_show = rs.set_limit(content, limit)
        self.assertEqual(number_of_news_to_show, len(content.entries))

    def test_limit_is_small(self):
        # Test case user pass limit that smaller than total number of news (3)
        content = mock.MagicMock()
        content.entries = td.TEST_ENTRIES
        limit = 2
        number_of_news_to_show = rs.set_limit(content, limit)
        self.assertEqual(number_of_news_to_show, 2)

    def test_limit_is_big(self):
        # Test case user pass limit that bigger than total number of news (3), should set number_of_news_to_show as
        # maximum, means len(content.entries)
        content = mock.MagicMock()
        content.entries = td.TEST_ENTRIES
        limit = 100500
        number_of_news_to_show = rs.set_limit(content, limit)
        self.assertEqual(number_of_news_to_show, len(content.entries))

    def test_limit_is_invalid(self):
        # Test case user pass 0 or negative int, should print user-friendly message and exit
        content = mock.MagicMock()
        content.entries = td.TEST_ENTRIES
        limit = -1
        with self.assertRaises(SystemExit):
            rs.set_limit(content, limit)


if __name__ == "__main__":
    unittest.main()
