import argparse
import logging
import requests
import sys
from bs4 import BeautifulSoup
import json
import os.path
import peewee
from datetime import datetime

try:
    from rss_reader.rss_parser import RssParser
    from rss_reader.db_worker import RssStorage, get_path
    from rss_reader.db_worker import db as rss_db

except ModuleNotFoundError:
    from rss_parser import RssParser
    from db_worker import RssStorage, get_path, db
    from db_worker import db as rss_db


def main(args=sys.argv[1:]):
    """Main function. Entry point of program"""
    arg_parser = get_arg_parser()
    parsed_arg = arg_parser.parse_args(args)
    if parsed_arg.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    check_limit(parsed_arg.limit)
    create_db()
    if parsed_arg.date:
        storage = get_storage(parsed_arg)
        news, items = get_news_from_storage(storage, parsed_arg)
    else:
        soup = get_soup(parsed_arg)
        storage = get_storage(parsed_arg, soup)
        news, items = get_news_from_storage(storage, parsed_arg)

    print_news(parsed_arg.json, news)


def get_arg_parser():
    """This function add console arguments"""
    parser = argparse.ArgumentParser(description='Python command-line RSS reader.')
    parser.add_argument('source', nargs='?', type=str, help='RSS URL')
    parser.add_argument('--version', '-v', help='Print version info', action='version', version='Version 0.4')
    parser.add_argument('--json', help='Print result as JSON', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', type=int, help='Limit news topics')
    parser.add_argument('--date', type=str, help='Print cached news')
    parser.add_argument('--to_html', type=str, help='Convert news to html file')
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
    try:
        if limit <= 0 or not limit:
            print('Invalid limit value. Please correct the limit value and try again')
            sys.exit(0)

    except TypeError:
        pass


def get_storage(parsed_arg, soup=None):
    """Function which return storage with news"""
    if parsed_arg.date:
        try:
            date = datetime.strptime(parsed_arg.date, '%Y%m%d')
        except ValueError:
            print('Invalid date. Please correct the date and try again')
            sys.exit(0)
        logging.info('Select news from DB.')

        with rss_db.connection_context():
            storage = RssStorage.select().where(RssStorage.pubDate == date).dicts()

            if not storage:
                print('No news for entered date')
                sys.exit(0)

    else:
        logging.info('Select news from URL.')
        rss_parser = RssParser(soup)
        storage = rss_parser.get_news()

    return storage


def get_news_from_storage(storage, parsed_arg):
    """Function which collect news"""
    news = dict()
    collected_items = list()
    for num, item in enumerate(storage):
        if parsed_arg.limit is None or num < parsed_arg.limit:
            if parsed_arg.json:
                news[num] = RssParser.json_format(item)

            else:
                news[num] = RssParser.default_format(item)
            collected_items.append(item)

        if not parsed_arg.date:
            try:
                with rss_db.connection_context():
                    RssStorage.create(**item)

            except peewee.IntegrityError:
                pass

    return news, collected_items


def print_news(arg_json, news):
    """Function which print news"""
    logging.info('Printing news.')
    if arg_json:
        print(json.dumps(news, indent=4, sort_keys=False, default=str))
    else:
        print(*news.values())


def get_soup(arg):
    """This function parse console arguments and create RssParser class"""
    try:
        logging.info('Try to get access to RSS feed')
        data_from_url = requests.get(arg.source)
        soup = BeautifulSoup(data_from_url.content, 'lxml-xml')
        if soup.find('rss'):
            return soup
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
