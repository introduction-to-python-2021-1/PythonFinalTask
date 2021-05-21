import os
import unittest
import io
import sys

import pandas as pd

try:
    from dataset import Data
except ImportError:
    from rss_reader.dataset import Data


class TestInit(unittest.TestCase):
    def test_init(self):
        self.test = Data.__init__
        self.assertTrue(self.test)


class TestFile(unittest.TestCase):
    def setUp(self):
        with self.assertWarns(ResourceWarning):
            self.test = Data()

    def test_file_clear(self):
        self.assertEqual(os.path.getsize("data.csv"), 0)

    def test_file(self):
        """File open"""
        with self.assertWarns(ResourceWarning):
            self.assertTrue(open("data.csv"))

    def test_date_empty(self):
        with self.assertRaises(SystemExit):
            self.assertEqual(self.test.print_data(20210519, 1, None), "Empty file")

    def tearDown(self):
        os.remove("data.csv")


class TestDataFrame(unittest.TestCase):
    def setUp(self):
        with self.assertWarns(ResourceWarning):
            self.test = Data()

    def test_dataframe(self):
        with self.assertRaises(IndexError):
            self.assertFalse(self.test.make_dataframe([1, 2]))

    def test_empty(self):
        """Test empty dataframe"""
        with self.assertRaises(IndexError):
            self.assertRaises(self.test.make_dataframe([]))

    def tearDown(self):
        os.remove("data.csv")


class TestLimit(unittest.TestCase):
    def setUp(self):
        with self.assertWarns(ResourceWarning):
            self.test = Data()

    def test_negative_limit(self):
        with self.assertRaises(SystemExit):
            self.assertLogs(self.test.print_data(20210518, -2, None))

    def tearDown(self):
        os.remove("data.csv")


class TestPrint(unittest.TestCase):
    def setUp(self):
        link_0 = 'https://news.yahoo.com/sheila-bridges-design-notes-122057672.html'
        link_1 = 'https://news.yahoo.com/george-floyd-square-1-later-192543800.html'
        link_2 = 'https://news.yahoo.com/ads-2021-hotel-awards-011339231.html'
        data = {"Date": ['2021-05-19T12:20:57Z', '2021-05-20T19:25:43Z', '2021-05-21T08:10:55Z'],
                "Link": [link_0, link_1, link_2],
                "Title": ['Sheila Bridges Design Notes', 'George Floyd Square 1 year later',"AD's 2021 Hotel Awards"]
                }
        self.test = pd.DataFrame(data)
        self.out = io.StringIO()
        sys.stdout = self.out

    def test_print(self):
        with self.assertWarns(ResourceWarning):
            self.ans = Data()
        self.ans.make_csv()
        self.ans.print_data(20210520, 2, None)
        self.assertTrue(self.out.getvalue())


if __name__ == "__main__":
    unittest.main()
