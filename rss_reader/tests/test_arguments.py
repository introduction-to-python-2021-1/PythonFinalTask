import unittest
from re import findall
from json import loads
from io import StringIO
from rss_reader import reader
from bs4 import BeautifulSoup
from contextlib import redirect_stdout
from ddt import ddt, unpack
from ddt import data as ddt_data


def create_test_data():
    data = str()
    for i in range(50):
        data += f'<item>\n<title>title {i}</title>' \
                '<link>https://news.yahoo.com/</link>' \
                '<pubDate>2021-05-27T20:06:59Z</pubDate>' \
                '<source url="https://news.yahoo.com/">Yahoo News</source>' \
                '<guid isPermaLink="false">biden-calls-out-republicans-who-have-taken-credit-for.html</guid>' \
                '<media:content url="https://s.yimg.com/os/creatr-uploaded-images/2021-05/b9e8f7c0-bf25-11eb""/>' \
                '<media:credit role="publishing company"/>' \
                '</item>'
    return data


@ddt
class TestRssArguments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arg_parser = reader.get_arg_parser()
        reader.create_db()
        cls.soup = BeautifulSoup(create_test_data(), 'lxml-xml')

    def test_version(self):
        """Tests --version argument"""
        with StringIO() as buf, redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                reader.main(args=['--version', ])
                self.assertEqual(buf.getvalue(), 'Version 1.0\n')

    def test_version_with_other_arg(self):
        """Tests --version argument with other"""
        with StringIO() as buf, redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                reader.main(args=['src', '--version', ])
                self.assertEqual(buf.getvalue(), 'Version 1.0\n')

    @ddt_data((['https://news.yahoo.com/rss', '--limit', '5', ], 5),
              (['https://news.yahoo.com/rss', '--limit', '100', ], 50),
              (['https://news.yahoo.com/rss', ], 50)
              )
    @unpack
    def test_default_output_with_limit(self, args, res):
        """Tests --limit argument"""
        parsed_arg = self.arg_parser.parse_args(args)
        select = reader.selection_from_url(self.soup)
        news, items = reader.collect_and_format_news(select, parsed_arg)
        with StringIO() as buf, redirect_stdout(buf):
            reader.print_news(parsed_arg.json, news)
            result_news_dates_and_links = findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), res)

    def test_json_output(self):
        """Tests --json argument"""
        args = ['https://news.yahoo.com/rss', '--json', ]
        parsed_arg = self.arg_parser.parse_args(args)
        select = reader.selection_from_url(self.soup)
        news, items = reader.collect_and_format_news(select, parsed_arg)
        with StringIO() as buf, redirect_stdout(buf):
            reader.print_news(parsed_arg.json, news)
            loads(buf.getvalue())

    @ddt_data((['https://news.yahoo.com/rss', '--limit', '5', '--json', ], 5),
              (['https://news.yahoo.com/rss', '--limit', '100', '--json', ], 50),
              (['https://news.yahoo.com/rss', '--json', ], 50)
              )
    @unpack
    def test_json_output_with_limit(self, args, res):
        """Tests --json argument and --limit"""
        parsed_arg = self.arg_parser.parse_args(args)
        select = reader.selection_from_url(self.soup)
        news, items = reader.collect_and_format_news(select, parsed_arg)
        with StringIO() as buf, redirect_stdout(buf):
            reader.print_news(parsed_arg.json, news)
            load = loads(buf.getvalue())
            self.assertEqual(len(load), res)


if __name__ == '__main__':
    unittest.main()
