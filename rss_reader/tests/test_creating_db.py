import unittest
import io
import os
import os.path
from rss_reader.rss_reader import create_db, get_storage, get_arg_parser, main
from rss_reader.db_worker import get_path
from contextlib import redirect_stdout
from test_arguments import create_test_data
from bs4 import BeautifulSoup


class TestRssReaderDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arg_parser = get_arg_parser()
        cls.soup = BeautifulSoup(create_test_data(), 'lxml-xml')

    def setUp(self):
        create_db()

    def tearDown(self):
        os.remove(get_path())

    def test_create_db(self):
        """Tests create DB"""
        self.assertTrue(os.path.isfile(get_path()))

    def test_version_with_other_arg(self):
        """Tests --version argument with other"""
        with io.StringIO() as buf, redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                main(args=['--date20210527', '--version', ])
                self.assertEqual(buf.getvalue(), 'Version 0.4\n')

    def test_invalid_date(self):
        """Tests --date argument with invalid value"""
        args = ['--date=20212222', ]
        parsed_arg = self.arg_parser.parse_args(args)
        with self.assertRaises(SystemExit):
            with io.StringIO() as buf, redirect_stdout(buf):
                get_storage(parsed_arg)
                self.assertEqual('Invalid date. Please correct the date and try again\n', buf.getvalue())

    def test_no_news_date(self):
        """Tests --date argument with no news"""
        args = ['--date=30210522', ]
        parsed_arg = self.arg_parser.parse_args(args)
        with self.assertRaises(SystemExit):
            with io.StringIO() as buf, redirect_stdout(buf):
                get_storage(parsed_arg)
                self.assertEqual('No news for entered date\n', buf.getvalue())


if __name__ == '__main__':
    unittest.main()
