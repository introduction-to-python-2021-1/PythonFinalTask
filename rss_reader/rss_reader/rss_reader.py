import argparse
import logging
import requests
import sys
from bs4 import BeautifulSoup
import json
from rss_reader.rss_parser import RssParser


def main(args=sys.argv[1:]):
    arg_parser = arg_parser_func()
    soup, parsed_arg = parse(arg_parser, args)
    collect_news_and_print(parsed_arg, soup)


def collect_news_and_print(parsed_arg, soup):
    rss_parser = RssParser(soup)
    news = dict()
    for num, item in enumerate(rss_parser.get_news()):
        if num == parsed_arg.limit:
            break

        if parsed_arg.json:
            news[num] = rss_parser.json_format(item)

        else:
            news[num] = rss_parser.default_format(item)

    if parsed_arg.json:
        print(json.dumps(news, indent=4, sort_keys=False, default=str))
    else:
        print(*news.values())


def arg_parser_func():
    """This function add console arguments"""
    parser = argparse.ArgumentParser(description='Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', '-v', help='Print version info', action='version', version='Version 0.2')
    parser.add_argument('--json', help='Print result as JSON', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', type=int, help='Limit news topics')
    return parser


def parse(parser, args):
    """This function parse console arguments and create RssParser class"""
    arg = parser.parse_args(args)

    try:
        if arg.limit <= 0:
            print('Invalid limit value. Please correct the limit value and try again')
            sys.exit(0)

    except TypeError:
        pass

    if arg.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    try:
        logging.info('Try to get access to RSS feed')
        data_from_url = requests.get(arg.source)
        soup = BeautifulSoup(data_from_url.content, 'lxml-xml')
        if soup.find('rss'):
            return soup, arg
        else:
            print('URL does not contain RSS')

    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print('Connection error. Please correct the URL and try again')
        sys.exit(0)

    except requests.exceptions.MissingSchema:
        print(f'Invalid URL {arg.source}: No schema supplied. Perhaps you meant http:{arg.source}?')
        sys.exit(0)


if __name__ == '__main__':
    main()
