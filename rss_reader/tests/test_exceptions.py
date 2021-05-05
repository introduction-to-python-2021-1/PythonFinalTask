import os
import unittest
from urllib.request import urlopen
from urllib.request import pathname2url

from rss_reader.rss_reader import logger
from rss_reader.rss_reader import get_response
from rss_reader.rss_reader import process_response


class TestExceptions(unittest.TestCase):
    """Tests that get_response and process_response functions from rss_reader handle exceptions."""

    def test_get_response(self):
        """Tests that get_response function handles response with bad status code (Ex: 404)."""
        url = "https://github.com/introduction-to-python-2021-1/PythonFinalTask/blob/main/wikipedia.org/wiki/RSS"

        with self.assertLogs(logger, "ERROR") as captured:
            with self.assertRaises(SystemExit):
                get_response(url)

            self.assertEqual("Couldn't get good response", captured.records[0].getMessage())

    def test_process_response(self):
        """Tests that process_response function handles response with wrong xml structure."""
        fake_response = urlopen("file:" + pathname2url(os.path.abspath("data/badsample.xml")))

        with self.assertLogs(logger, "ERROR") as captured:
            with self.assertRaises(SystemExit):
                process_response(fake_response, None)

            self.assertEqual("Couldn't parse response", captured.records[0].getMessage())

        fake_response.close()


if __name__ == "__main__":
    unittest.main()
