"""This module is the entry point to the utility"""

from parser import Parser
from feed import Feed
from bs4 import BeautifulSoup
import requests
import logging

if __name__ == '__main__':
    parser = Parser()
    args = parser.parse_args()
    visibility = args.verbose
    to_json = args.json
    if visibility:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)
    logger = logging
    if args.source:
        source_url = args.source
        limit = args.limit
        if limit:
            limit = int(limit)
        try:
            logger.info(' Sending GET request to the specified URL')
            response = requests.get(source_url)
        except requests.exceptions.ConnectionError:
            logger.error(' An error occurred while sending a GET request to the specified URL. Check the specified URL'
                         ' and your internet connection')
        else:
            logger.info(' Parsing XML from the specified URL')
            soup = BeautifulSoup(response.content, 'lxml-xml')
            feed_title = soup.find('title').text
            items = soup.find_all('item')
            logger.info(f' Founded {len(items)} news items')
            if items:
                feed = Feed(feed_title, items, to_json, logger, limit)
                print(feed)
            logger.info(' Successfully completed')
