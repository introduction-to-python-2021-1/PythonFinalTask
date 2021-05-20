'''Entry module of programm'''
import argparse
import logging
import requests
import sys

from .rssparser import RssParser


def main():
    '''This function add console arguments'''
    parser = argparse.ArgumentParser(description='Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', '-v', help='Print version info', action='version', version='Version 0.1')
    parser.add_argument('--json', help='Print result as JSON', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', type=int, help='Limit news topics')
    parse(parser)


def parse(parser):
    '''This function parse console arguments'''
    arg = parser.parse_args(sys.argv[1:])

    if arg.limit == 0:
        print('Invalid limit value. Plase correct the limit value and try again')
        sys.exit(0)

    if arg.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    try:
        logging.info('Try to get acces to RSS feed')
        document = requests.get(arg.source)
        RssParser(document, arg, logging)

    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL) as e:
        print('Connection error. Please correct the URL and try again')

    except requests.exceptions.MissingSchema as e:
        print(e)


if __name__ == '__main__':
    main()
