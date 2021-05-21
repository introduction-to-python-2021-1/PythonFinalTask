import os
import unittest
try:
    from dataset import Data
except ImportError:
    from rss_reader.dataset import Data


class TestProcessResponse(unittest.TestCase):
    def setUp(self):
        with self.assertWarns(ResourceWarning):
            self.test = Data()

    def test_init(self):
        with self.assertWarns(ResourceWarning):
            self.test.__init__()
            self.assertTrue(self.test)

    def test_file_clear(self):
        self.assertEqual(os.path.getsize("data.csv"), 0)

    def test_file(self):
        """File open"""
        with self.assertWarns(ResourceWarning):
            self.assertTrue(open("data.csv"))

    def test_date_empty(self):
        with self.assertRaises(SystemExit):
            self.assertEqual(self.test.print_data(20210519, 1, None), "Empty file")

    def test_dataframe(self):
        with self.assertRaises(IndexError):
            self.assertFalse(self.test.make_dataframe([1, 2]))

    def tearDown(self):
        os.remove("data.csv")


if __name__ == "__main__":
    unittest.main()
