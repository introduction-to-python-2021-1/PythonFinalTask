import os
import io
import sys
import json
import unittest
from unittest.mock import patch, Mock
from urllib.error import URLError
from urllib.error import HTTPError

import ddt

from rss_reader import channel_parse

@ddt.ddt
@patch.object(channel_parse, "urlopen")
class TestGetResponse(unittest.TestCase):
    """Tests get_response function from rss_reader."""

    def test_get_response_with_valid_url(self, mocked):
        """Tests that get_response function from rss_reader closes connection after successful response from server."""
        mocked.return_value = response_mock = Mock()
        channel_parse.get_xml_tree("https://news.yahoo.com/rss/")
        response_mock.close.assert_called()