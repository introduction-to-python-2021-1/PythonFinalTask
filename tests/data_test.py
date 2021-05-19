import io
import unittest
import sys
from rss_reader.dataset import Data


class TestProcessResponse(unittest.TestCase):
        def setUp(self):
            self.a = Data()
            self.out = io.StringIO()
            sys.stdout = self.out

        def test_data_frame(self):

            self.assertTrue(self.a.make_dataframe([1, 2, 3]))
