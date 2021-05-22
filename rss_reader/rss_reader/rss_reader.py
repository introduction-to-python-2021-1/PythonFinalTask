"""This module is the entry point to the utility"""

import logging
import sys

from bs4 import BeautifulSoup
import requests

from components.converter import Converter
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
    if args.date:
        feed = Feed(args.source, args.date, args.limit, args.json, logger)
        if args.to_pdf:
            converter = Converter(logger)
            converter.to_pdf(args.to_pdf, feed, args.limit)
        if args.to_html:
            converter = Converter(logger)
            converter.to_html(args.to_html, feed, args.limit)
        print(feed)
    elif args.source:
        soup = get_data_from_url(logger, args.source)
        if soup:
            feed_title = soup.find('title').text
            items = soup.find_all('item')
            logger.info(f' Founded {len(items)} news items')
            if items:
                feed = Feed(args.source, args.date, args.limit, args.json, logger, feed_title, items)
                if args.to_pdf:
                    converter = Converter(logger)
                    converter.to_pdf(args.to_pdf, feed, args.limit)
                if args.to_html:
                    converter = Converter(logger)
                    converter.to_html(args.to_html, feed, args.limit)
                print(feed)
            logger.info(' Successfully completed')
    else:
        logger.error(' Source URL not specified. Please check your input and try again')


def get_data_from_url(logger, url):
    try:
        logger.info(' Sending GET request to the specified URL')
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logger.error(' An error occurred while sending a GET request to the specified URL. Check the specified URL'
                     ' and your internet connection')
    except requests.exceptions.MissingSchema:
        logger.error(f' Invalid URL "{url}". The specified URL should look like "http://www.example.com/"')
    else:
        logger.info(' Parsing XML from the specified URL')
        soup = BeautifulSoup(response.content, 'lxml-xml')
        if soup.find('rss'):
            return soup
        else:
            logger.error(' Specified URL does not contain RSS. Please check the specified URL and try again')
    return None


if __name__ == '__main__':
    main()
