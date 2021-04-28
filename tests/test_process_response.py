import os
import unittest
from urllib.request import *
from rss_reader import logger
from rss_reader import process_response

logger.disabled = True


class TestProcessResponse(unittest.TestCase):
    """Tests process_response function from rss_reader with limit set to various values."""

    def setUp(self):
        """Opens connection with example.xml to create fake response for process_response."""
        self.fake_response = urlopen("file:" + pathname2url(os.path.abspath("tests/example.xml")))

    def test_none_limit(self):
        """Tests process_response from rss_reader with limit set to None."""
        self.assertEqual(len(process_response(self.fake_response, None)["Items"]), 2, "Wrong output size")

    def test_negative_limit(self):
        """Tests process_response from rss_reader with limit set to -1."""
        self.assertEqual(len(process_response(self.fake_response, -1)["Items"]), 0, "Wrong output size")

    def test_zero_limit(self):
        """Tests process_response from rss_reader with limit set to 0."""
        self.assertEqual(len(process_response(self.fake_response, 0)["Items"]), 0, "Wrong output size")

    def test_adequate_positive_limit_1(self):
        """Tests process_response from rss_reader with limit set to 1."""
        self.assertEqual(len(process_response(self.fake_response, 1)["Items"]), 1, "Wrong output size")

    def test_adequate_positive_limit_2(self):
        """Tests process_response from rss_reader with limit set to 2."""
        self.assertEqual(len(process_response(self.fake_response, 2)["Items"]), 2, "Wrong output size")

    def test_inadequate_positive_limit(self):
        """Tests process_response from rss_reader with limit set to 100."""
        self.assertEqual(len(process_response(self.fake_response, 100)["Items"]), 2, "Wrong output size")

    def tearDown(self):
        """Closes connection with example.xml."""
        self.fake_response.close()


if __name__ == "__main__":
    unittest.main()
