
import unittest
import io
import rss_reader.reader as reader
import re
import json

from contextlib import redirect_stdout


class TestRssReader(unittest.TestCase):
    def test_version(self):
        """Tests --version argument"""
        with io.StringIO() as buf, redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                reader.main(args=['--version', ])
                self.assertEqual(buf.getvalue(), 'Version 0.2\n')

    def test_version_with_other_arg(self):
        """Tests --version argument with other"""
        with io.StringIO() as buf, redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                reader.main(args=['src', '--version', ])
                self.assertEqual(buf.getvalue(), 'Version 0.2\n')

    def test_limit(self):
        """Tests --limit argument"""
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.main(args=['https://news.yahoo.com/rss/', '--limit=5', ])
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 5)

    def test_large_limit(self):
        """Tests --limit argument large than feed size"""
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.main(args=['https://news.yahoo.com/rss/', '--limit=100', ])
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 50)

    def test_without_limit(self):
        """Tests without --limit argument"""
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.main(args=['https://news.yahoo.com/rss/', ])
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 50)

    def test_json_output(self):
        """Tests --json argument"""
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.main(args=['https://news.yahoo.com/rss/', '--json', ])
            try:
                json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')

    def test_json_output_with_limit(self):
        """Tests --json argument and --limit"""
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.main(args=['https://news.yahoo.com/rss/', '--json', '--limit=5'])
            try:
                res = json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')
            else:
                self.assertEqual(len(res), 5)

    def test_json_output_without_limit(self):
        """Tests --json argument without --limit"""
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.main(args=['https://news.yahoo.com/rss/', '--json'])
            try:
                res = json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')
            else:
                self.assertEqual(len(res), 50)

    def test_json_output_large_limit(self):
        """Tests --json argument and large --limit"""
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.main(args=['https://news.yahoo.com/rss/', '--json', '--limit=555'])
            try:
                res = json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')
            else:
                self.assertEqual(len(res), 50)


if __name__ == '__main__':
    unittest.main()
