"""
    This module covers with tests code of reader.py
"""
import unittest
import requests
from unittest.mock import patch
from unittest.mock import MagicMock
from io import StringIO
from rss_core.reader import SiteReader


class TestReader(unittest.TestCase):
    """ Tests for SiteReader """

    def test_get_data_empty_link(self):
        reader = SiteReader()
        reader.get_data()


    # @patch('sys.stdout', new_callable=StringIO)
    # def test_get_data_empty_link(self, mock_stdout):
    #     reader = SiteReader()
    #     with self.assertRaises(SystemExit) as cm:
    #         reader.get_data()
    #     self.assertEqual(cm.exception.code, 1)
    #     self.assertEqual("[ERROR] Value error has occurred while getting data from chanel",
    #                      mock_stdout.getvalue().strip())
