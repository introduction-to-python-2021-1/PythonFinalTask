import logging
import os
import unittest
import io
import sys

import pandas.errors
import pandas as pd

from rss_reader.dataset import Data


class TestFile(unittest.TestCase):
    def setUp(self):
        with self.assertWarns(ResourceWarning):
            self.data = Data()

    def test_file_clear(self):
        """Test clear file"""
        self.assertEqual(os.path.getsize("data.csv"), 0)

    def test_date_empty(self):
        """Test Empty result"""
        with self.assertRaises(pandas.errors.EmptyDataError):
            self.assertEqual(
                self.data.sort_data(
                    20210519, 1, None), "Empty file")

    def tearDown(self):
        os.remove("data.csv")


class TestDataFrame(unittest.TestCase):
    def setUp(self):
        link_0 = 'https://news.yahoo.com/sheila-bridges-design-notes-122057672.html'
        link_1 = 'https://news.yahoo.com/george-floyd-square-1-later-192543800.html'
        link_2 = 'https://news.yahoo.com/ads-2021-hotel-awards-011339231.html'
        self.feed = {"Date": ['2021-05-19T12:20:57Z', '2021-05-20T19:25:43Z', '2021-05-21T08:10:55Z'],
                     "Link": [link_0, link_1, link_2],
                     "Title": ['Sheila Bridges Design Notes', 'George Floyd Square 1 year later',
                               "AD's 2021 Hotel Awards"]
                     }
        self.test = pd.DataFrame(self.feed)
        with self.assertWarns(ResourceWarning):
            self.data = Data()
        self.out = io.StringIO()
        sys.stdout = self.out

    def test_dataframe(self):
        """Test input on dataframe"""
        self.assertIsNone(self.data.append_dataframe(self.feed))

    def tearDown(self):
        os.remove("data.csv")


class TestArg(unittest.TestCase):
    def setUp(self):
        with self.assertWarns(ResourceWarning):
            self.data = Data()

    def test_verbose(self):
        """Test verbose lvl"""
        with self.assertRaises(pandas.errors.EmptyDataError):
            self.assertLogs(self.data.sort_data(20210523, 1, logging.INFO), logging.INFO)

    def test_negative_limit(self):
        """Test negative limit"""
        with self.assertRaises(pandas.errors.EmptyDataError):
            self.assertIsNone(self.data.sort_data(20210523, -2, None))

    def tearDown(self):
        os.remove("data.csv")


class TestVerbose(unittest.TestCase):
    def test_log(self):
        """Test error log"""
        with self.assertWarns(ResourceWarning):
            self.data = Data()
        with self.assertRaises(AssertionError):
            with self.assertRaises(AssertionError):
                self.assertLogs(self.data.update_cache(), "ERROR:root:Empty file")

    def tearDown(self):
        os.remove("data.csv")


if __name__ == "__main__":
    unittest.main()
