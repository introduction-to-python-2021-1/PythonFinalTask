import unittest
from io import StringIO
from os import remove
from datetime import datetime
from re import findall
from json import loads
from rss_reader import reader
from rss_reader.db_worker import get_path, RssStorage
from rss_reader.db_worker import db as rss_db
from contextlib import redirect_stdout
from ddt import ddt, unpack
from ddt import data as ddt_data


@ddt
class TestRssReaderDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arg_parser = reader.get_arg_parser()
        reader.create_db()
        with rss_db.connection_context():
            RssStorage.create_table()
        for i in range(50):
            with rss_db.connection_context():
                RssStorage.create(**{
                                     'title': f'title {i}',
                                     'link': 'https://news.yahoo.com/.html',
                                     'pubDate': datetime(2021, 5, 30),
                                     'media': 'https://s.yimg.com/os/creatr-uploaded-images'}
                                  )

    @classmethod
    def tearDownClass(cls):
        remove(get_path())

    @ddt_data((['--date=20210530', '--limit', '5', ], 5),
              (['--date=20210530', '--limit', '100', ], 50),
              (['--date=20210530', ], 50)
              )
    @unpack
    def test_news_limit(self, args, res):
        """Tests --date with limit"""
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            result_news_dates_and_links = findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), res)

    def test_json_news(self):
        """Tests --date with --json printing"""
        args = ['--date=20210530', '--json', ]
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            loads(buf.getvalue())

    @ddt_data((['--date=20210530', '--limit', '5', '--json', ], 5),
              (['--date=20210530', '--limit', '100', '--json', ], 50),
              (['--date=20210530', '--json', ], 50)
              )
    @unpack
    def test_json_news_no_limit(self, args, res):
        """Tests --date with --json with --limit"""
        parsed_arg = self.arg_parser.parse_args(args)
        storage = reader.selection_from_db(parsed_arg.date)
        news, items = reader.collect_and_format_news(storage, parsed_arg)
        with StringIO() as buf, redirect_stdout(buf):
            reader.selection_from_db(parsed_arg.date)
            reader.print_news(parsed_arg.json, news)
            load = loads(buf.getvalue())
            self.assertEqual(len(load), res)


if __name__ == '__main__':
    unittest.main()
