"""This module is the entry point to the utility"""

import logging
import sys

import requests
from bs4 import BeautifulSoup

from components.feed import Feed
from components.parser import Parser


def main(argv=sys.argv[1:]):
    """This function is a entry point"""
    parser = Parser()
    args = parser.parse_args(argv)
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)
    logger = logging
    if isinstance(args.limit, int) and args.limit < 1:
        logger.error(f' The limit argument must be greater than zero ({args.limit} was passed)')
        sys.exit()
    if args.source:
        try:
            logger.info(' Sending GET request to the specified URL')
            response = requests.get(args.source)
        except requests.exceptions.ConnectionError:
            logger.error(' An error occurred while sending a GET request to the specified URL. Check the specified URL'
                         ' and your internet connection')
        except requests.exceptions.MissingSchema:
            logger.error(f' Invalid URL "{args.source}". The specified URL should look like "http://www.example.com/"')
        else:
            logger.info(' Parsing XML from the specified URL')
            soup = BeautifulSoup(response.content, 'lxml-xml')
            if soup.find('rss'):
                feed_title = soup.find('title').text
                items = soup.find_all('item')
                logger.info(f' Founded {len(items)} news items')
                if items:
                    feed = Feed(feed_title, items, args.json, logger, args.limit)
                    print(feed)
                logger.info(' Successfully completed')
            else:
                logger.error(' Specified URL does not contain RSS. Please check the specified URL and try again')
    else:
        logger.error(' Source URL not specified. Please check your input and try again')


if __name__ == '__main__':
    main()
