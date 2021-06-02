import os
import sys
import unittest
from unittest.mock import patch, Mock
from argparse import Namespace
from contextlib import contextmanager
from io import StringIO
from rss_reader.rss_reader import *


@contextmanager
def captured_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


class TestRssReader(unittest.TestCase):

    def test_verbose_args(self):
        args = Namespace(rss_url='https://www.theguardian.com/world/rss', json=False, verbose=True, limit=1)

        with captured_output() as (out):
            verbose_args(args)

        output = out.getvalue().strip()
        self.assertIn('Verbosity is turned on.', output)

    def test_print_news(self):
        data = {
            "Feed": "Feed",
            "News": [
                {
                    "Title": "Title",
                    "Date": "Date",
                    "Link": "Link",
                    "Images": []
                }
            ],
        }

        with captured_output() as (out):
            print_news(data)

        output = out.getvalue().strip()
        self.assertIn('Count of news:', output)

    @patch("rss_reader.rss_reader.requests.get")
    def test_get_response(self, mock_make_request):
        mock_make_request.return_value.status_code = 200
        response = get_response('https://www.theguardian.com/world/rss')
        self.assertEqual(response.status_code, 200)

    def test_extract_xml(self):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(file_dir, 'rss-test-theguardian.xml')
        with open(filename, "r") as file:
            content = file.read()
        self.assertIsInstance(extract_xml(content, 0), dict)
        self.assertEqual(len(extract_xml(content, 0)["News"]), 41)
        self.assertIsInstance(extract_xml(content, 0)["News"][0], dict)

    def test_print_json(self):
        data = {}
        result_print_json = print_json(data)
        self.assertEqual(result_print_json, "{}")

        data = {"a": "b"}
        result_print_json = print_json(data)
        self.assertEqual(result_print_json, '{\n   "a": "b"\n}')


if __name__ == "__main__":
    unittest.main()
