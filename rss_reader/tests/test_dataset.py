import logging
import os
import unittest
import io
import sys

import pandas as pd

try:
    from dataset import Data
except ImportError:
    from rss_reader.dataset import Data


class TestFile(unittest.TestCase):
    def setUp(self):
        with self.assertWarns(ResourceWarning):
            self.test = Data()

    def test_file_clear(self):
        """Test clear file"""
        self.assertEqual(os.path.getsize("data.csv"), 0)

    def test_date_empty(self):
        """Test Empty result"""
        with self.assertRaises(SystemExit):
            self.assertEqual(
                self.test.print_data(
                    20210519, 1, None, None), "Empty file")

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
        self.assertIsNone(self.data.make_dataframe(self.feed))

    def test_print(self):
        """Testing no date print """
        with self.assertWarns(ResourceWarning):
            self.ans = Data()
        self.test.to_csv("data.csv", index=False)
        with self.assertRaises(SystemExit):
            self.ans.print_data(20210526, 1, None, None)
            self.assertEqual(self.out.getvalue(), "doesnt have news on this day (20210526)")

    def tearDown(self):
        os.remove("data.csv")


class TestArg(unittest.TestCase):
    def setUp(self):
        with self.assertWarns(ResourceWarning):
            self.data = Data()

    def test_verbose(self):
        """Test verbose lvl"""
        with self.assertRaises(SystemExit):
            self.assertLogs(self.data.print_data(20210523, 1, logging.INFO, None), logging.INFO)

    def test_json(self):
        """Test json"""
        with self.assertRaises(SystemExit):
            self.assertIs(self.data.print_data(20210523, 1, None, "--json"), None)

    def test_negative_limit(self):
        """Test negative limit"""
        with self.assertRaises(SystemExit):
            self.assertIsNone(self.data.print_data(20210523, -2, None, None))

    def tearDown(self):
        os.remove("data.csv")


class Testinit(unittest.TestCase):
    def test_log(self):
        """Test error log"""
        with self.assertWarns(ResourceWarning):
            self.data = Data()
        with self.assertRaises(SystemExit):
            self.assertLogs(self.data.make_csv(), "ERROR:root:Empty file")

if __name__ == "__main__":
    unittest.main()
