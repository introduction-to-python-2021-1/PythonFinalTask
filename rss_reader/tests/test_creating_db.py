import unittest
import io
import os
import os.path
from time import sleep
from rss_reader.rss_reader import create_db, get_storage, get_arg_parser, get_news_from_storage, print_news
from rss_reader.db_worker import get_path
from contextlib import redirect_stdout
import re
from test_arguments import create_test_data
from bs4 import BeautifulSoup


class TestRssReaderDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arg_parser = get_arg_parser()

    def setUp(self):
        create_db()
        generator = create_test_data()
        self.soup = BeautifulSoup(next(generator), 'lxml-xml')

    def tearDown(self):
        os.remove(get_path())

    def test_create_db(self):
        self.assertTrue(os.path.isfile(get_path()))

    def test_invalid_date(self):
        args = ['--date=20212222', ]
        parsed_arg = self.arg_parser.parse_args(args)
        with self.assertRaises(SystemExit):
            with io.StringIO() as buf, redirect_stdout(buf):
                get_storage(parsed_arg)
                self.assertEqual('Invalid date. Please correct the date and try again\n', buf.getvalue())

    def test_no_news_date(self):
        args = ['--date=30210522', ]
        parsed_arg = self.arg_parser.parse_args(args)
        with self.assertRaises(SystemExit):
            with io.StringIO() as buf, redirect_stdout(buf):
                get_storage(parsed_arg)
                self.assertEqual('No news for entered date\n', buf.getvalue())

    def test_news_limit(self):
        args = ['src', '--limit=5', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = get_storage(parsed_arg, self.soup)
        news, items = get_news_from_storage(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            get_storage(parsed_arg)
            print_news(parsed_arg.json, news)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 5)

    # def test_negative_limit(self):
    #     with self.assertRaises(SystemExit):
    #         with io.StringIO() as buf, redirect_stdout(buf):
    #             main(args=['src', '--limit', '-1', ])
    #             self.assertEqual(buf.getvalue(), 'Invalid limit value. Please correct the limit value and try again\n')
    #
    # def test_zero_limit(self):
    #     with self.assertRaises(SystemExit):
    #         with io.StringIO() as buf, redirect_stdout(buf):
    #             main(args=['src', '--limit', '0', ])
    #             self.assertEqual(buf.getvalue(), 'Invalid limit value. Please correct the limit value and try again\n')
    #
    # def test_invalid_schema_url(self):
    #     with self.assertRaises(SystemExit):
    #         with io.StringIO() as buf, redirect_stdout(buf):
    #             main(args=['url.com'])
    #             self.assertEqual(buf.getvalue(),
    #                              'Invalid URL url.com: No schema supplied. Perhaps you meant http:url.com?\n')
    #
    # def test_invalid_url(self):
    #     with self.assertRaises(SystemExit):
    #         with io.StringIO() as buf, redirect_stdout(buf):
    #             main(args=['https://ttt.com'])
    #             self.assertEqual(buf.getvalue(), 'Connection error. Please correct the URL and try again\n')


if __name__ == '__main__':
    unittest.main()
