import unittest
import io
import re
import json
from rss_reader.rss_reader import main, collect_news_and_print, arg_parser_func

from bs4 import BeautifulSoup
from contextlib import redirect_stdout


def create_test_data():
    data = str()
    for _ in range(50):
        data += '<item>\n<title>title</title>' \
                '<link>https://news.yahoo.com/</link>' \
                '<pubDate>2021-05-27T20:06:59Z</pubDate>' \
                '<source url="https://news.yahoo.com/">Yahoo News</source>' \
                '<guid isPermaLink="false">biden-calls-out-republicans-who-have-taken-credit-for.html</guid>' \
                '<media:content url="https://s.yimg.com/os/creatr-uploaded-images/2021-05/b9e8f7c0-bf25-11eb""/>' \
                '<media:credit role="publishing company"/>' \
                '</item>'
    return data


class TestRssReader(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(create_test_data(), 'lxml-xml')

    def test_version(self):
        """Tests --version argument"""
        with io.StringIO() as buf, redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                main(args=['--version', ])
                self.assertEqual(buf.getvalue(), 'Version 0.2\n')

    def test_version_with_other_arg(self):
        """Tests --version argument with other"""
        with io.StringIO() as buf, redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                main(args=['src', '--version', ])
                self.assertEqual(buf.getvalue(), 'Version 0.2\n')

    def test_limit(self):
        """Tests --limit argument"""
        args = ['https://news.yahoo.com/rss', '--limit=5', ]
        arg_parser = arg_parser_func()
        with io.StringIO() as buf, redirect_stdout(buf):
            parsed_arg = arg_parser.parse_args(args)
            collect_news_and_print(parsed_arg, self.soup)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 5)

    def test_large_limit(self):
        """Tests --limit argument large than feed size"""
        args = ['https://news.yahoo.com/rss', '--limit=100', ]
        arg_parser = arg_parser_func()
        with io.StringIO() as buf, redirect_stdout(buf):
            parsed_arg = arg_parser.parse_args(args)
            collect_news_and_print(parsed_arg, self.soup)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 50)

    def test_without_limit(self):
        """Tests without --limit argument"""
        args = ['https://news.yahoo.com/rss', ]
        arg_parser = arg_parser_func()
        with io.StringIO() as buf, redirect_stdout(buf):
            parsed_arg = arg_parser.parse_args(args)
            collect_news_and_print(parsed_arg, self.soup)
            result_news_dates_and_links = re.findall('Date: .+\nLink: .+\n', buf.getvalue())
            self.assertEqual(len(result_news_dates_and_links), 50)

    def test_json_output(self):
        """Tests --json argument"""
        args = ['https://news.yahoo.com/rss', '--json', ]
        arg_parser = arg_parser_func()
        with io.StringIO() as buf, redirect_stdout(buf):
            parsed_arg = arg_parser.parse_args(args)
            collect_news_and_print(parsed_arg, self.soup)
            try:
                json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')

    def test_json_output_with_limit(self):
        """Tests --json argument and --limit"""
        args = ['https://news.yahoo.com/rss', '--json', '--limit=5', ]
        arg_parser = arg_parser_func()
        with io.StringIO() as buf, redirect_stdout(buf):
            parsed_arg = arg_parser.parse_args(args)
            collect_news_and_print(parsed_arg, self.soup)
            try:
                res = json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')
            else:
                self.assertEqual(len(res), 5)

    def test_json_output_without_limit(self):
        """Tests --json argument without --limit"""
        args = ['https://news.yahoo.com/rss', '--json', ]
        arg_parser = arg_parser_func()
        with io.StringIO() as buf, redirect_stdout(buf):
            parsed_arg = arg_parser.parse_args(args)
            collect_news_and_print(parsed_arg, self.soup)
            try:
                res = json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')
            else:
                self.assertEqual(len(res), 50)

    def test_json_output_large_limit(self):
        """Tests --json argument and large --limit"""
        args = ['https://news.yahoo.com/rss', '--json', '--limit=555', ]
        arg_parser = arg_parser_func()
        with io.StringIO() as buf, redirect_stdout(buf):
            parsed_arg = arg_parser.parse_args(args)
            collect_news_and_print(parsed_arg, self.soup)
            try:
                res = json.loads(buf.getvalue())
            except json.JSONDecodeError:
                self.fail('JSON Decode Error')
            else:
                self.assertEqual(len(res), 50)


if __name__ == '__main__':
    unittest.main()
