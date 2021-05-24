
import argparse
import logging
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rss_reader.rss_parser import RssParser


def main(args):
    """This function add console arguments"""
    parser = argparse.ArgumentParser(description='Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', '-v', help='Print version info', action='version', version='Version 0.2')
    parser.add_argument('--json', help='Print result as JSON', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', type=int, help='Limit news topics')
    parse(parser, args)


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
        document = requests.get(arg.source)
        RssParser(document, arg, logging)

    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print('Connection error. Please correct the URL and try again')

    except requests.exceptions.MissingSchema:
        print(f'Invalid URL {arg.source}: No schema supplied. Perhaps you meant http:{arg.source}?')


if __name__ == '__main__':
    main(sys.argv[1:])
