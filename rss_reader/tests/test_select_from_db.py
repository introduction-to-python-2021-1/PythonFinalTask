import unittest
import io
import os
import os.path
import peewee
import datetime
from rss_reader.rss_reader import create_db, get_storage, get_arg_parser, get_news_from_storage, print_news
from rss_reader.db_worker import get_path, RssStorage
from rss_reader.db_worker import db as rss_db
from contextlib import redirect_stdout
import re
import json
from test_arguments import create_test_data
from bs4 import BeautifulSoup


class TestRssReaderDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arg_parser = get_arg_parser()
        create_db()
        with rss_db.connection_context():
            RssStorage.create_table()
        for item in range(50):
            try:
                with rss_db.connection_context():
                    RssStorage.create(**{
                                         'title': f'title {item}',
                                         'link': 'https://news.yahoo.com/.html',
                                         'pubDate': datetime.datetime(2021, 5, 30),
                                         'media': 'https://s.yimg.com/os/creatr-uploaded-images'}
                                      )

            except peewee.IntegrityError:
                pass

        cls.soup = BeautifulSoup(create_test_data(), 'lxml-xml')

    @classmethod
    def tearDownClass(cls):
        os.remove(get_path())

    def test_news_limit(self):
        """Tests --date with limit"""
        args = ['--date=20210530', '--limit=5', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = get_storage(parsed_arg, self.soup)
        news, items = get_news_from_storage(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            get_storage(parsed_arg)
            print_news(parsed_arg.json, news)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 5)

    def test_news_no_limit(self):
        """Tests --date without limit"""
        args = ['--date=20210530', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = get_storage(parsed_arg, self.soup)
        news, items = get_news_from_storage(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            get_storage(parsed_arg)
            print_news(parsed_arg.json, news)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 50)

    def test_news_large_limit(self):
        """Tests --date with large limit"""
        args = ['--date=20210530', '--limit=999']
        parsed_arg = self.arg_parser.parse_args(args)
        storage = get_storage(parsed_arg, self.soup)
        news, items = get_news_from_storage(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            get_storage(parsed_arg)
            print_news(parsed_arg.json, news)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 50)

    def test_json_news(self):
        """Tests --date with --json printing"""
        args = ['--date=20210530', '--json', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = get_storage(parsed_arg, self.soup)
        news, items = get_news_from_storage(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            get_storage(parsed_arg)
            print_news(parsed_arg.json, news)
            try:
                json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')

    def test_json_news_no_limit(self):
        """Tests --date with --json without limit"""
        args = ['--date=20210530', '--json', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = get_storage(parsed_arg, self.soup)
        news, items = get_news_from_storage(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            get_storage(parsed_arg)
            print_news(parsed_arg.json, news)
            try:
                res = json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')
            else:
                self.assertEqual(len(res), 50)

    def test_json_news_large_limit(self):
        """Tests --date with --json wit large limit"""
        args = ['--date=20210530', '--json', '--limit=999']
        parsed_arg = self.arg_parser.parse_args(args)
        storage = get_storage(parsed_arg, self.soup)
        news, items = get_news_from_storage(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            get_storage(parsed_arg)
            print_news(parsed_arg.json, news)
            try:
                res = json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')
            else:
                self.assertEqual(len(res), 50)


if __name__ == '__main__':
    unittest.main()
