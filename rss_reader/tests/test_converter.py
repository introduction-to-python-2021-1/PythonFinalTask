"""
Module with tests for converter module
"""

import os
import sys
import unittest

# Make tests crossplatform
sys.path.append(os.getcwd())

from main_reader import converter
import data_for_tests as td


class MyTestCase(unittest.TestCase):
    """
    Class of tests for converter
    """

    def test_make_html(self):
        # Test expected variable was passed to template and successfully rendered
        for one_news in td.TEST_NEWSDICT:
            rendered = converter.make_html(td.TEST_NEWSDICT, one_news)
        self.assertTrue("Yahoo News - Latest News & Headlines" in rendered)

    def test_save_pdf_right(self):
        # Test html file was rendered and converted to pdf in a right way
        self.assertFalse(converter.safe_pdf(os.getcwd(), td.TEST_NEWSDICT, 1))


if __name__ == '__main__':
    unittest.main()
