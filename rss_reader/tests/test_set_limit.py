import json
import unittest

import ddt

from rss_reader.rss_reader import set_limit


@ddt.ddt
class TestSetLimit(unittest.TestCase):
    """Tests set_limit function from rss_reader with limit set to various values."""

    @ddt.data((None, 9), (-1, 0), (0, 0), (1, 1), (9, 9), (10, 9))
    @ddt.unpack
    def test_set_limit(self, limit, expected):
        """Tests set_limit function from rss_reader with limit set to various values."""
        with open("data/news.json") as json_file:
            channel_info_and_items = json.load(json_file)

        self.assertEqual(len(set_limit(channel_info_and_items, limit)["Items"]), expected, "Wrong output size")


if __name__ == "__main__":
    unittest.main()
