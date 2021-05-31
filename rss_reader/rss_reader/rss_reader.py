"""This module is the entry point to the utility"""

import logging
import sys

from bs4 import BeautifulSoup
from colorlog import ColoredFormatter
import requests

from components.cache import Cache
from components.converter import Converter
from components.feed import Feed
from components.parser import Parser


def main(argv=sys.argv[1:]):
    """
    This function is a entry point

    Parameters:
        argv (list): List of command-line arguments
    """
    parser = Parser()
    args = parser.parse_args(argv)
    log_handler = logging.StreamHandler()
    if args.verbose:
        logging.root.setLevel(logging.INFO)
    else:
        logging.root.setLevel(logging.ERROR)
    if args.colorize:
        log_handler.setFormatter(
            ColoredFormatter('%(log_color)s%(levelname)s%(reset)s | %(log_color)s%(message)s%(reset)s'))
    else:
        log_handler.setFormatter(logging.Formatter('%(levelname)s | %(message)s'))
    logger = logging.getLogger('root')
    logger.addHandler(log_handler)
    converter = Converter(logger)
    cache = Cache(logger)
    if args.date:
        feeds_list = cache.get_news_from_cache(args.date, args.source, args.limit, args.json, args.colorize)
        if args.to_pdf is not None:
            converter.to_pdf(args.to_pdf, feeds_list, args.limit)
        if args.to_html is not None:
            converter.to_html(feeds_list, args.limit, path=args.to_html)
        for feed in feeds_list:
            print(feed)
    elif args.source:
        soup = get_data_from_url(logger, args.source)
        if soup:
            feed_title = soup.find('title').text
            items = soup.find_all('item')
            logger.info(f'Founded {len(items)} news items')
            if items:
                feed = Feed(args.source, args.limit, args.json, args.colorize, logger, feed_title, cache,
                            news_items=items)
                if args.to_pdf is not None:
                    converter.to_pdf(args.to_pdf, [feed], args.limit)
                if args.to_html is not None:
                    converter.to_html([feed], args.limit, path=args.to_html)
                print(feed)
            logger.info('Successfully completed')
    else:
        logger.error('Source URL not specified. Please check your input and try again')


def get_data_from_url(logger, source_url):
    """
    This function parsing RSS from specified URL

    Parameters:
        logger (module): logging module
        source_url (str): Link to RSS Feed

    Returns:
        bs4.BeautifulSoup: Object of class bs4.BeautifulSoup containing parsed RSS feed
        None: If specified URL does not contain RSS, invalid URL or connection error
    """
    try:
        logger.info('Sending GET request to the specified URL')
        response = requests.get(source_url)
    except requests.exceptions.ConnectionError:
        logger.error('An error occurred while sending a GET request to the specified URL. Check the specified URL'
                     ' and your internet connection')
    except requests.exceptions.MissingSchema:
        logger.error(f'Invalid URL "{source_url}". The specified URL should look like "http://www.example.com/"')
    else:
        logger.info('Parsing XML from the specified URL')
        soup = BeautifulSoup(response.content, 'lxml-xml')
        if soup.find('rss'):
            return soup
        else:
            logger.error('Specified URL does not contain RSS. Please check the specified URL and try again')
    return None


if __name__ == '__main__':
    main()
