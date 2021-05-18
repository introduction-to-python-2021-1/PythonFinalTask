import unittest
from unittest import mock
from unittest.mock import patch

import feedparser
from rss_reader import rss_reader as rs

NEWSLINK = "https://news.yahoo.com/rss/"
TEST_ENTRIES = [{'title': 'On-duty police officer sexually assaulted by gas station manager, Georgia cops say',
                 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://news.yahoo.com/rss/',
                                  'value': 'On-duty police officer sexually assaulted by gas station manager, Georgia cops say'},
                 'links': [{'rel': 'alternate', 'type': 'text/html',
                            'href': 'https://news.yahoo.com/duty-police-officer-sexually-assaulted-010634049.html'}],
                 'link': 'https://news.yahoo.com/duty-police-officer-sexually-assaulted-010634049.html',
                 'published': '2021-05-18T01:06:34Z',
                 'source': {'href': 'https://www.kentucky.com/', 'title': 'Lexington Herald-Leader'},
                 'id': 'duty-police-officer-sexually-assaulted-010634049.html', 'guidislink': False, 'media_content': [
        {'height': '86',
         'url': 'https://s.yimg.com/uu/api/res/1.2/A3riyROEGQuSpO0M838c0g--~B/aD02NDE7dz0xMTQwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/lexington_herald_leader_mcclatchy_articles_314/d453d37647ec075638a8bc71a3e80ce0',
         'width': '130'}], 'media_credit': [{'role': 'publishing company'}], 'credit': ''},
                {'title': 'Heroic Dog Who Lost Her Snout Saving Two Girls Years Ago Passes Away in the Philippines',
                 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://news.yahoo.com/rss/',
                                  'value': 'Heroic Dog Who Lost Her Snout Saving Two Girls Years Ago Passes Away in the Philippines'},
                 'links': [{'rel': 'alternate', 'type': 'text/html',
                            'href': 'https://news.yahoo.com/heroic-dog-lost-her-snout-151239087.html'}],
                 'link': 'https://news.yahoo.com/heroic-dog-lost-her-snout-151239087.html',
                 'published': '2021-05-18T15:12:39Z',
                 'source': {'href': 'https://nextshark.com/', 'title': 'NextShark'},
                 'id': 'heroic-dog-lost-her-snout-151239087.html', 'guidislink': False, 'media_content': [
                    {'height': '86',
                     'url': 'https://s.yimg.com/uu/api/res/1.2/rSALC6BHE5GLgr.puYJEuA--~B/aD00MjU7dz04MDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/nextshark_articles_509/1939d15898adc9f02b3aa5266f51881a',
                     'width': '130'}], 'media_credit': [{'role': 'publishing company'}], 'credit': ''},
                {'title': '600,000 kids between 12 and 15 have received Pfizer vaccine dose since FDA authorization',
                 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://news.yahoo.com/rss/',
                                  'value': '600,000 kids between 12 and 15 have received Pfizer vaccine dose since FDA authorization'},
                 'links': [{'rel': 'alternate', 'type': 'text/html',
                            'href': 'https://news.yahoo.com/600-000-kids-between-12-151913054.html'}],
                 'link': 'https://news.yahoo.com/600-000-kids-between-12-151913054.html',
                 'published': '2021-05-18T15:19:13Z', 'source': {'href': 'https://www.axios.com/', 'title': 'Axios'},
                 'id': '600-000-kids-between-12-151913054.html', 'guidislink': False, 'media_content': [{'height': '86',
                                                                                                         'url': 'https://s.yimg.com/uu/api/res/1.2/u194wekMUQEk_9oy8lv3Iw--~B/aD03MjA7dz0xMjgwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/axios_articles_623/0ed6f0918ef60763f094e36c4bcc43f4',
                                                                                                         'width': '130'}],
                 'media_credit': [{'role': 'publishing company'}], 'credit': ''}]


class TestMainReader(unittest.TestCase):
    """
TODO: write normal description after add all tests
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
        content.entries = TEST_ENTRIES
        rs.printing_parsing_news(content, 1)
        news = mock_print.call_args_list
        self.assertEqual(len(news), (1 * 5) + 1)

    @patch("builtins.print", autospec=True, side_effect=print)
    def test_limit_really_three(self, mock_print):
        # Test number of output lines is equal limit * 5 (number of lines in one news WITHOUT logs no json)
        content = mock.MagicMock()
        content.entries = TEST_ENTRIES
        rs.printing_parsing_news(content, 3)
        news = mock_print.call_args_list
        self.assertEqual(len(news), (3 * 5) + 1)

    # Tests for function "printing_parsing_news_in_json"
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_printing_parsing_news_in_json(self, mock_print):
        # Test output have the first key of our json dictionary ("news"), which is not present in the regular output
        content = mock.MagicMock()
        content.entries = TEST_ENTRIES
        rs.printing_parsing_news_in_json(content, 1)
        first_new = mock_print.call_args_list[0].args[0]
        self.assertTrue("news" in first_new)


if __name__ == "__main__":
    unittest.main()
