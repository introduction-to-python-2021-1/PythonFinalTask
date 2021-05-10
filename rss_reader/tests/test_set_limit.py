import json
import unittest

import ddt

from rss_reader.rss_reader import limit_news_items


@ddt.ddt
class TestLimitNewsItems(unittest.TestCase):
    """Tests limit_news_items function from rss_reader with limit set to various values."""

    @ddt.data((None, 9), (-1, 0), (0, 0), (1, 1), (9, 9), (10, 9))
    @ddt.unpack
    def test_limit_news_items(self, limit, expected):
        """Tests set_limit function from rss_reader with limit set to various values."""
        with open("data/news.json") as json_file:
            news_items = json.load(json_file)

        self.assertEqual(len(limit_news_items(news_items, limit)), expected, "Wrong output size")


if __name__ == "__main__":
    unittest.main()
