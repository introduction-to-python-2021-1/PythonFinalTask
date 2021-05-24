
import unittest
import io
import rss_reader.reader as reader

from contextlib import redirect_stdout


class TestRssReader(unittest.TestCase):
    def test_negative_limit(self):
        with self.assertRaises(SystemExit):
            with io.StringIO() as buf, redirect_stdout(buf):
                reader.main(args=['src', '--limit', '-1', ])
                self.assertEqual(buf.getvalue(), 'Invalid limit value. Please correct the limit value and try again\n')

    def test_zero_limit(self):
        with self.assertRaises(SystemExit):
            with io.StringIO() as buf, redirect_stdout(buf):
                reader.main(args=['src', '--limit', '0', ])
                self.assertEqual(buf.getvalue(), 'Invalid limit value. Please correct the limit value and try again\n')

    def test_invalid_schema_url(self):
        with io.StringIO() as buf, redirect_stdout(buf):
                reader.main(args=['url.com'])
                self.assertEqual(buf.getvalue(),
                                 'Invalid URL url.com: No schema supplied. Perhaps you meant http:url.com?\n')

    def test_invalid_url(self):
        with io.StringIO() as buf, redirect_stdout(buf):
                reader.main(args=['https://ttt.com'])
                self.assertEqual(buf.getvalue(), 'Connection error. Please correct the URL and try again\n')


if __name__ == '__main__':
    unittest.main()
