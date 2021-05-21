import os
import unittest
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


if __name__ == "__main__":
    unittest.main()
