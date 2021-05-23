"""
    This module covers with tests code of reader.py
"""
import requests
import unittest
from unittest.mock import MagicMock
from rss_core.reader import SiteReader


class TestReader(unittest.TestCase):
    """ Tests for SiteReader """

    pass

    # def test_bad_response_code(self):
    #     response = requests.Response()
    #     response.status_code = 404
    #     requests.get = MagicMock(return_value=response)
    #     reader = SiteReader()
    #     self.assertRaises(ConnectionError, reader.get_data, "http://")
