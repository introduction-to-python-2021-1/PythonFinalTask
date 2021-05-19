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

news_print = ("title", "date", "summary", "description", "image", "content_of_media", "link")

def set_limit(content, limit):
    """Set limit for news"""
    limit_of_news = len(content.entries)
    if limit == 0 or limit <= 0:
        raise ValueError("Insert volume of news to read")
    elif limit <= len(content.entries):
        limit_of_news = limit
    return limit_of_news

def print_news(content, limit_of_news):
    """Print news on console"""
    print("\n" + content.feed.title + "\n")
    for news in content.entries[:limit_of_news]:
        for item in news_print:
            if item in news.keys():
                print(item.capitalize() + ":" + str(news[item]))
                print("\n")

def main():
    """ Calls the main function with the required arguments"""
    arguments = create_parser()

if __name__ == "__main__":
    # Run the reader
    main()