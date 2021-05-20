import argparse
import json
import sys
import logging
import logging.handlers
from urllib.error import URLError
import requests

import feedparser

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logger = None

def create_logger(verbose):
    """Creates a logger"""
    global logger
    if logger is None:
        logger = logging.getLogger()
    return logger

def command_arguments_parser():
    """ Adds positional and optional arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 1.0")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")
    arguments = parser.parse_args()
    return arguments

news_print = ("title", "date", "summary", "description", "image", "content_of_media", "link")

def set_limit(content, limit):
    """Set limit for news"""
    len_of_news = len(content.entries)
    if limit == 0 or limit <= 0:
        raise ValueError("Insert volume of news to read")
    elif limit <= len(content.entries):
        len_of_news = limit
    return len_of_news

def print_news(content, limit_of_news):
    """Print news on console"""
    if not content.json:
        print("\n" + content.feed.title + "\n")
        for news in content.entries[:limit_of_news]:
            for part in news_print:
                if part in news.keys():
                    print(part.capitalize() + ":" + str(news[part]))
                    print("\n")
    elif content.json:
        json_dict = {}
        newslist = []
        newsdict = {}
        for news in content.entries[:limit_of_news]:
            for part in news_print:
                if part in news.keys():
                    json_dict[part.capitalize()] = news[part]
            newslist.append(json_dict.copy())
        newsdict["news"] = newslist
        print(json.dumps(newsdict, indent=1))


def create_rss_link(source, verbose):
    """ Gets a link with RSS news and parses it, prints logs"""
    logger = create_logger(verbose)
    try:
        content = feedparser.parse(source)
        if not source:
            raise ValueError
        logger.info(f"Reads the link {source}")
    except URLError as e:
        logger.error(f"Error {e} in trying to open link {source}")
        return print("Change link and try again, please")
    except ValueError as e:
        logger.error(f"Error {e} in trying to open link {source}")
        return print("Add rss link, please")
    return content

def main():
    arguments = command_arguments_parser()
    logger = create_logger(arguments.verbose)
    content = create_rss_link(arguments.source, arguments.verbose)
    number_of_news = set_limit(content, arguments.limit)
    if arguments.limit:
        logger.info(f"Would read only {arguments.limit} number of news")
    if arguments.json:
        logger.info(f"Convert news in json format")
        print_news(content, number_of_news)
    else:
        print_news(content, number_of_news)
    logger.info(f"End of reading")

if __name__ == "__main__":
    # Run the reader
    main()

