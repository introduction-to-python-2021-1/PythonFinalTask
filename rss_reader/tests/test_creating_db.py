import unittest
from io import StringIO
from os import remove
from os.path import isfile
from rss_reader import reader
from rss_reader.db_worker import get_path
from contextlib import redirect_stdout
from bs4 import BeautifulSoup
from tests.test_arguments import create_test_data


class TestRssReaderDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arg_parser = reader.get_arg_parser()
        cls.soup = BeautifulSoup(create_test_data(), 'lxml-xml')

    def setUp(self):
        reader.create_db()

    def tearDown(self):
        remove(get_path())

    def test_create_db(self):
        """Tests create DB"""
        self.assertTrue(isfile(get_path()))

    def test_version_with_other_arg(self):
        """Tests --version argument with other"""
        with StringIO() as buf, redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                reader.main(args=['--date20210527', '--version', ])
                self.assertEqual(buf.getvalue(), 'Version 1.0\n')

    def test_invalid_date(self):
        """Tests --date argument with invalid value"""
        args = ['--date=20212222', ]
        parsed_arg = self.arg_parser.parse_args(args)
        with self.assertRaises(SystemExit):
            with StringIO() as buf, redirect_stdout(buf):
                reader.selection_from_db(parsed_arg.date)
                self.assertEqual('Invalid date. Please correct the date and try again\n', buf.getvalue())

    def test_no_news_date(self):
        """Tests --date argument with no news"""
        args = ['--date=30210522', ]
        parsed_arg = self.arg_parser.parse_args(args)
        with self.assertRaises(SystemExit):
            with StringIO() as buf, redirect_stdout(buf):
                reader.selection_from_db(parsed_arg.date)
                self.assertEqual('No news for entered date\n', buf.getvalue())


if __name__ == '__main__':
    unittest.main()
