import unittest
from urllib.request import urlopen

from rss_reader.rss_reader import get_response


class TestGetResponse(unittest.TestCase):
    """Tests get_response function from rss_reader."""

    def test_get_response(self):
        """Tests that get_response successfully gets response from server."""
        url = "https://www.google.com/"
        self.assertEqual(get_response(url).code, 200, "Wrong output size")


if __name__ == "__main__":
    unittest.main()
