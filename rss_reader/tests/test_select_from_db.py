import unittest
import io
import os
import os.path
import peewee
import datetime
import re
import json
from rss_reader import reader
from rss_reader.db_worker import get_path, RssStorage
from rss_reader.db_worker import db as rss_db
from contextlib import redirect_stdout


class TestRssReaderDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arg_parser = reader.get_arg_parser()
        reader.create_db()
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

    @classmethod
    def tearDownClass(cls):
        os.remove(get_path())

    def test_news_limit(self):
        """Tests --date with limit"""
        args = ['--date=20210530', '--limit=5', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 5)

    def test_news_no_limit(self):
        """Tests --date without limit"""
        args = ['--date=20210530', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 50)

    def test_news_large_limit(self):
        """Tests --date with large limit"""
        args = ['--date=20210530', '--limit=999']
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 50)

    def test_json_news(self):
        """Tests --date with --json printing"""
        args = ['--date=20210530', '--json', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            try:
                json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')

    def test_json_news_no_limit(self):
        """Tests --date with --json without limit"""
        args = ['--date=20210530', '--json', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            res = json.loads(buf.getvalue())
            self.assertEqual(len(res), 50)

    def test_json_news_large_limit(self):
        """Tests --date with --json wit large limit"""
        args = ['--date=20210530', '--json', '--limit=999']
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with io.StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            res = json.loads(buf.getvalue())
            self.assertEqual(len(res), 50)


if __name__ == '__main__':
    unittest.main()
