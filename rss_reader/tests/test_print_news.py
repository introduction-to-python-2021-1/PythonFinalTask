import io
import sys
import unittest

from rss_reader.rss_reader import print_news


class TestPrintNews(unittest.TestCase):
    """Tests print_news fucntion from rss_reader."""

    def test_print_news(self):
        """Tests that print_news properly prints list with news items."""
        # Create data for testing
        test_list = [
            {
                "Feed": "TUT.BY: Новости Витебска и Витебской области",
                "Title": "В Орше взорвали старое здание одного из предприятий",
                "Date": "Mon, 10 May 2021 12:52:00 +0300",
                "Link": "https://news.tut.by/culture/"
            }
        ]
        test_output = "".join((
            "\nFeed: TUT.BY: Новости Витебска и Витебской области\n",
            "Title: В Орше взорвали старое здание одного из предприятий\n",
            "Date: Mon, 10 May 2021 12:52:00 +0300\n",
            "Link: https://news.tut.by/culture/\n"
        ))
        # Create StringIO object and redirects stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        # Perform testing
        print_news(test_list)
        self.assertEqual(captured_output.getvalue(), test_output)
        # Resets redirect of stdout
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
