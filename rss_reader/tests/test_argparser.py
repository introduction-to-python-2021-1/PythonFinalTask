import datetime
import unittest
import uuid
from argparse import ArgumentParser
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, Mock

from modules.argparser import Argparser


class TestArgprser(TestCase):
    """ Class for testing the module for parsing arguments """
    def setUp(self) -> None:
        self.argparser = Argparser(logger=Mock())
        self.parser = ArgumentParser()
        self.tomorrow_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')
        # self.error = self.parser.error(message=Mock())
        self.random_dir = str(uuid.uuid4())

    @patch('sys.stderr', new_callable=StringIO)
    def test_empty_source(self, mock_stderr):
        """ Check for passing an empty string instead of url """
        args = ['']
        with self.assertRaises(SystemExit):
            self.argparser.parse_arguments(args)
        self.assertIn('the following arguments are required: source', mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_wrong_date_format(self, mock_stderr):
        """ Check for passing date of incorrect format """
        args = ['--date=2021-05-31']
        with self.assertRaises(SystemExit):
            self.argparser.parse_arguments(args)
        self.assertIn("time data '2021-05-31' does not match format '%Y%m%d'", mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_wrong_date(self, mock_stderr):
        """ Check for transmission of the future date """
        args = ['--date={}'.format(self.tomorrow_date)]
        with self.assertRaises(SystemExit):
            self.argparser.parse_arguments(args)
        self.assertIn('date cannot be more than today', mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_wrong_directory(self, mock_stderr):
        """ Check for a non-existent directory """
        args = ['https://news.yahoo.com/rss/', '--to-html={}'.format(self.random_dir)]
        with self.assertRaises(SystemExit):
            self.argparser.parse_arguments(args)
        self.assertIn('directory "{}" does not exist'.format(self.random_dir), mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
