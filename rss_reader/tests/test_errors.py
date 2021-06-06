import unittest
from io import StringIO
from os import remove
from rss_reader.reader import main
from contextlib import redirect_stdout
from ddt import ddt
from ddt import data as ddt_data
from rss_reader.db_worker import get_path


@ddt
class TestRssReaderErrors(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        remove(get_path())

    @ddt_data('-1', '0', )
    def test_negative_limit(self, lim):
        with self.assertRaises(SystemExit):
            with StringIO() as buf, redirect_stdout(buf):
                main(args=['src', '--limit', lim, ])
                self.assertEqual(buf.getvalue(), 'Invalid limit value. Please correct the limit value and try again\n')

    @ddt_data('url.com', 'https://ttt.com', 'ttt', )
    def test_invalid_schema_url(self, url):
        with self.assertRaises(SystemExit):
            with StringIO() as buf, redirect_stdout(buf):
                main(args=[url])
                self.assertEqual(buf.getvalue(), 'Invalid URL {url}. Please correct the URL and try again\n')


if __name__ == '__main__':
    unittest.main()
