import argparse
import os
import sys
import logging.handlers
from urllib.error import URLError

import feedparser

import sqlite3

import datetime

from reader.functions import parse_news, make_json, check_limit, execute_news


def main():
    """Creating logger"""
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler('../../../logs.txt')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.disable()

    """Creating connection to DB and cursor object"""
    connection = sqlite3.connect('news.db')
    cursor = connection.cursor()

    """Checking the current version of the program"""
    new_version = 1.0

    if not os.path.exists('../../../actual_version.txt'):
        with open('../../../actual_version.txt', 'w') as act_version:
            act_version.write(str(new_version))
        print('Creating file for storing actual programm version')
    else:
        with open('../../../actual_version.txt', 'r+') as act_version:
            actual = act_version.read()
            act_version.seek(0)
            new_version = round((float(actual) + 0.1), 1)
            act_version.write(str(new_version))

    """Create command line arguments"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + str(new_version), help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, nargs='?', default='', help='Sets the date the news will be displayed')

    # args = parser.parse_args()

    args, unknown = parser.parse_known_args()

    # print(args)
    # print(unknown)

    if args.limit:
        limit = check_limit(args.limit)
    else:
        limit = 0

    if args.verbose:
        """Turning on the output of messages about events"""
        logging.disable(0)
        logger.info('Parcing news...')

    result = []
    try:
        rss_news = feedparser.parse(args.source)
        result = parse_news(rss_news.entries, cursor, connection)
    except URLError:
        print("Source isn't available")

    if args.date:
        try:
            args_date = (datetime.datetime.strptime(args.date, '%Y%m%d')).date()
            logger.info(
                f"Retrieves news for the selected date ({args_date}) ...")
            result = execute_news(args.date, cursor)
            if len(result) == 0:
                print(f"Sorry, there are no articles for {args_date}!")
        except ValueError:
            print('Please, enter the date in the following format: "YYYYMMDD".')
            result = []
    if limit > 0:
        logger.info(f'Working with limited by user number ({limit} items) of articles')
        logger.info('Creating the list of news for limited articles...')
        for item in result[0:limit]:
            if args.json:
                json_item = make_json(item)
                print(json_item)
            else:
                print(item)
        logger.info('The list of news was created successfully!')
    elif args.json:
        logger.info('Creating the list of news in json format...')
        for item in result:
            json_item = make_json(item)
            print(json_item)
        logger.info('The list of news was created successfully!')
    else:
        logger.info('Creating the list of news...')
        for article in result:
            print(article)
        logger.info('The list of news was created successfully!')


if __name__ == '__main__':
    main()
