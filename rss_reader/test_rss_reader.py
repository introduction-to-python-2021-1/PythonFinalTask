import os
import sys
import unittest
from unittest.mock import patch
from contextlib import contextmanager
from io import StringIO
from rss_reader.rss_reader import rss_reader


@contextmanager
def captured_output():
    """Capture and return STDOUT"""
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


class TestRssReader(unittest.TestCase):
    """Test functions from the module 'rss_reader.py'"""

    @patch("rss_reader.rss_reader.rss_reader.get_response")
    def test_get_response(self, mock_make_request):
        """Test the function 'get_response' with correct URL"""
        mock_make_request.return_value.status_code = 200
        response = rss_reader.get_response('https://www.theguardian.com/world/rss')
        self.assertEqual(response.status_code, 200)

    def test_extract_data_from_xml(self):
        """Test the function 'extract_data_from_xml', the correct structure of returned dictionary"""
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(file_dir, 'rss-test-theguardian.xml')
        with open(filename, "r") as file:
            content = file.read()
        self.assertIsInstance(rss_reader.extract_data_from_xml(content, 0), dict)
        self.assertEqual(len(rss_reader.extract_data_from_xml(content, 0)["News"]), 41)
        self.assertIsInstance(rss_reader.extract_data_from_xml(content, 0)["News"][0], dict)

    def test_extract_data_from_bad_xml(self):
        """Test the function 'extract_data_from_xml' with bad xml, SystemExit is rising"""
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(file_dir, 'rss-test-bad.xml')
        with open(filename, "r") as file:
            content = file.read()
        with self.assertRaises(SystemExit):
            rss_reader.extract_data_from_xml(content, 0)

    def test_print_json(self):
        """Test the function 'print_json', the correct output of dictionary"""
        data = {}
        result_print_json = rss_reader.print_json(data)
        self.assertIn("{}", result_print_json)

        data = {"a": "b"}
        result_print_json = rss_reader.print_json(data)
        self.assertIn('{\n   "a": "b"\n}', result_print_json)

    def test_print_news(self):
        """Test the function 'print_news', the correct output of all data items of the dictionary"""
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
        with captured_output() as out:
            rss_reader.print_news(data)
        output = out.getvalue().strip()
        expected_print_news = "Feed: Feed \n\nTitle: Title\nDate: Date\nLink: Link\nImages: 0"
        self.assertIn(expected_print_news, output)


if __name__ == "__main__":
    unittest.main()
