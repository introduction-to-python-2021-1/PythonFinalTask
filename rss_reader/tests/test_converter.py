""" Module with tests for converter module. """
import os
import sys
import unittest

# Make tests crossplatform
sys.path.append(os.getcwd())  # noqa E402

from main_reader import converter
import data_for_tests as td


class TestConverter(unittest.TestCase):
    """ Tests for rendering html template and convert newsdict to html and pdf format"""

    def test_make_html(self):
        """ Test expected variable was passed to template and successfully rendered. """
        for one_news in td.TEST_NEWSDICT:
            rendered = converter.make_html(td.TEST_NEWSDICT, one_news)
        self.assertTrue("Yahoo News - Latest News & Headlines" in rendered)

    def test_save_pdf_right(self):
        """ Test html file was rendered and converted to pdf in a right way. """
        self.assertFalse(converter.save_pdf(os.getcwd(), td.TEST_NEWSDICT, 1))

    def test_html_error_raised_with_a_wrong_path(self):
        """ Test FileNotFoundError is raising if user pass the wrong path to a directory with '--to-html'. """
        with self.assertRaises(FileNotFoundError):
            converter.save_html("some_wrong_path", td.TEST_NEWSDICT, 1)

    def test_pdf_error_raised_with_a_wrong_path(self):
        """ Test FileNotFoundError is raising if user pass the wrong path to a directory with '--to-pdf'. """
        with self.assertRaises(FileNotFoundError):
            converter.save_pdf("some_wrong_path", td.TEST_NEWSDICT, 1)


if __name__ == '__main__':
    unittest.main()
