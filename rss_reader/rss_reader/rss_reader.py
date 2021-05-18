import argparse
import json
import sys
import logging
import logging.handlers
from urllib.error import URLError

import feedparser

def create_parser(args):
    """ Adds positional and optional arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 1.0")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")

    return parser.parse_args(args)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def check_url(url_feed):
    """ The function gets a link to the rss feed and returns the feed using feedparser"""
    try:
        logger.info(f"click {url_feed}")
        feed_url = feedparser.parse(url_feed)
    except URLError:
        logger.error(f"can't found {url_feed}")
        sys.exit()
    return feed_url