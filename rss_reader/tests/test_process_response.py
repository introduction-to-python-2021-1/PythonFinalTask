import os
import unittest
from urllib.request import urlopen
from urllib.request import pathname2url

from ddt import ddt
from ddt import data
from ddt import unpack

from rss_reader import process_response


@ddt
class TestProcessResponse(unittest.TestCase):
    """Tests process_response function from rss_reader with limit set to various values."""

    def setUp(self):
        """Opens connection with example.xml to create fake response for process_response."""
        self.fake_response = urlopen("file:" + pathname2url(os.path.abspath("data/goodsample.xml")))

    @data((None, 9), (-1, 0), (0, 0), (1, 1), (9, 9), (10, 9))
    @unpack
    def test_process_response(self, limit, expected):
        self.assertEqual(len(process_response(self.fake_response, limit)["Items"]), expected, "Wrong output size")

    def tearDown(self):
        """Closes connection with example.xml."""
        self.fake_response.close()


if __name__ == "__main__":
    unittest.main()
