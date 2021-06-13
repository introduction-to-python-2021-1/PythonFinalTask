from io import StringIO
import sys
import unittest
from rss_reader import local_storage


class TestLocalSrorage(unittest.TestCase):

    def setUp(self):
        self.lc_st = local_storage.LocalStorage()

    def test_get_news_type(self):
        self.assertIsInstance(self.lc_st.get_news_by_date_from_locale_storage("20210613"), list)

    def test_get_news_by_date_size(self):
        self.assertTrue(len(self.lc_st.get_news_by_date_from_locale_storage("20210612")) == 18)

    # def test_print_news_by_date_from_local_storage(self):
    #
    #     test_output = "".join((
    #         "1\n",
    #         "Title: Netanyahu uses last speech as prime minister to attack Biden on Iran\n",
    #         "Date: 2021-06-13T15:21:14Z\n",
    #         "Link: https://news.yahoo.com/netanyahu-uses-last-speech-prime-152114681.html"
    #     ))
    #
    #     captured_output = StringIO()
    #     sys.stdout = captured_output
    #     self.lc_st.print_news_from_storage_by_date("20210613", 1)
    #     self.assertEqual(captured_output.getvalue().rstrip(), test_output)
    #     # Resets redirect of stdout
    #     sys.stdout = sys.__stdout__
