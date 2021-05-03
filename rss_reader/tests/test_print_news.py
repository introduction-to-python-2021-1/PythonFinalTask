import io
import sys
import unittest
from rss_reader import print_news


class TestPrintNews(unittest.TestCase):
    """Tests print_news fucntion from rss_reader."""

    def setUp(self):
        """Creates StringIO object and redirects stdout."""
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def test_print_news(self):
        """Tests that print_news properly prints dictionary with channel info and items."""
        test_dict = {
            "Title": "Yahoo News - Latest News & Headlines",
            "Items": [
                {
                    "Title": "AP sources: Feds search Rudy Giuliani's NYC home, office",
                    "Date": "2021-04-28T16:26:16Z",
                    "Link": "https://news.yahoo.com/ap-source-feds-execute-warrant-162616009.html"
                }
            ]
        }
        test_output = "".join((
            "\nFeed: Yahoo News - Latest News & Headlines\n\n",
            "Title: AP sources: Feds search Rudy Giuliani's NYC home, office\n",
            "Date: 2021-04-28T16:26:16Z\n",
            "Link: https://news.yahoo.com/ap-source-feds-execute-warrant-162616009.html\n"
        ))

        print_news(test_dict)
        self.assertEqual(self.captured_output.getvalue(), test_output)

    def tearDown(self):
        """Resets redirect of stdout."""
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
