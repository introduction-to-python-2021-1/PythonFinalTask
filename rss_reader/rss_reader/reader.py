import argparse
import logging
import requests
import sys
from bs4 import BeautifulSoup
import json
import os.path
import peewee
from datetime import datetime
from urllib.parse import urlparse
from rss_reader.parser import RssParser
from rss_reader.db_worker import RssStorage, get_path
from rss_reader.db_worker import db as rss_db
from rss_reader.converter import save_html, save_pdf
from termcolor import colored


def main(args=sys.argv[1:]):
    """Main function. Entry point of program"""
    args.append('--colorize')
    arg_parser = get_arg_parser()
    parsed_arg = arg_parser.parse_args(args)
    if parsed_arg.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    check_limit(parsed_arg.limit)
    create_db()
    if parsed_arg.date:
        select = selection_from_db(parsed_arg.date)
        news, items = collect_and_format_news(select, parsed_arg)
    else:
        url_verification(parsed_arg.source)
        request = get_response(parsed_arg.source)
        soup = get_soup(request)
        select = selection_from_url(soup)
        news, items = collect_and_format_news(select, parsed_arg)

    print_news(parsed_arg.json, parsed_arg.colorize, news)
    if parsed_arg.to_html:
        save_html(items, parsed_arg.to_html, datetime.now().strftime("%m.%d %H.%M.%S"))

    if parsed_arg.to_pdf:
        save_pdf(items, parsed_arg.to_pdf, datetime.now().strftime("%m.%d %H.%M.%S"))


def get_arg_parser():
    """This function add console arguments"""
    parser = argparse.ArgumentParser(description='Python command-line RSS reader.')
    parser.add_argument('source', nargs='?', type=str, help='RSS URL')
    parser.add_argument('--version', '-v', help='Print version info', action='version', version='Version 1.0')
    parser.add_argument('--json', help='Print result as JSON', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', type=int, help='Limit news topics')
    parser.add_argument('--date', type=str, help='Print cached news')
    parser.add_argument('--to_html', type=str, help='Convert news to html file. Path example "d:/folder')
    parser.add_argument('--to_pdf', type=str, help='Convert news to html file. Path example "d:/folder')
    parser.add_argument('--colorize', help='Print colorize result', action='store_true')
    return parser


def create_db():
    """Function which create DB if it doesn't exist"""
    if not os.path.isfile(get_path()):
        logging.info('Create SQLite DB to store news.')
        with rss_db.connection_context():
            RssStorage.create_table()


def check_limit(limit):
    """Function which check --limit arg"""
    logging.info('Check limit value.')
    if limit and limit <= 0:
        print('Invalid limit value. Please correct the limit value and try again')
        sys.exit(0)


def selection_from_db(date):
    """Function which return news selection form db """
    try:
        date = datetime.strptime(date, '%Y%m%d')
    except ValueError:
        print('Invalid date. Please correct the date and try again')
        sys.exit(0)
    logging.info('Select news from DB.')

    with rss_db.connection_context():
        select = RssStorage.select().where(RssStorage.pubDate == date).dicts()
        if not select:
            print('No news for entered date')
            sys.exit(0)

    return select


def selection_from_url(soup):
    """Function which return news selection form """
    logging.info('Select news from URL.')
    rss_parser = RssParser(soup)
    select = rss_parser.select_news()
    return select


def collect_and_format_news(select, parsed_arg):
    """Function which return news from select"""
    news = dict()
    collected_items = list()
    for num, item in enumerate(select):
        if not parsed_arg.date:
            try:
                with rss_db.connection_context():
                    RssStorage.create(**item)

            except peewee.IntegrityError:
                pass

        if parsed_arg.limit is None or num < parsed_arg.limit:
            collected_items.append(item)
            if parsed_arg.json:
                news[num] = RssParser.json_format(item)

            else:
                news[num] = RssParser.default_format(item, parsed_arg.colorize)
    return news, collected_items


def print_news(arg_json, arg_color, news):
    """Function which print news"""
    logging.info('Printing news.')
    if arg_json:
        if arg_color:
            print(colored(json.dumps(news, indent=4, sort_keys=False, default=str), "green", "on_grey"))

    else:
        print(*news.values())


def url_verification(url):
    """This function verify URL"""
    logging.info('Verify URL')
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        print(f'Invalid URL {url}. Please correct the URL and try again')
        sys.exit(0)


def get_response(source):
    """This function return request.content"""
    try:
        response = requests.get(source)
        return response.content
    except requests.exceptions.ConnectionError:
        print(f'Invalid URL {source}. Please correct the URL and try again')
        sys.exit(0)


def get_soup(response):
    """This function return soup"""
    logging.info('Get access to RSS feed')
    soup = BeautifulSoup(response, 'lxml-xml')
    if soup.find('rss'):
        return soup
    else:
        print('URL does not contain RSS')


if __name__ == '__main__':
    main()
