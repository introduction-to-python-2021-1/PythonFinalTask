import argparse
import sys
import logging
import json
import os
from urllib.error import URLError


import feedparser

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

try:
    from dataset import Data
except ImportError:
    from rss_reader.dataset import Data


data = Data()


def create_parser(args):
    """ Create positional and optional arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 3.0")
    parser.add_argument("url", type=str, nargs="?", help="URL ")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--date", type=str)
    return parser.parse_args(args)


def open_url(url):
    """ Try to open url
    :param url page
    :return feed of news"""

    try:
        logger.info(f"open {url} and start parse")
        feed = feedparser.parse(url)
    except URLError:
        logger.error(f"cant open or found {url}")
        sys.exit()
    except Exception:
        logger.error(f"exception: {Exception}")
        sys.exit()

    return feed


def print_news(args):
    """Check format and print news on console or json
    :param args from the user"""
    feed = open_url(args.url)
    try:
        if not args.json:
            print(f'Feed: {feed["channel"]["title"]}')
        else:
            print("JSON")
            print(json.dumps(feed["channel"]["title"], indent=3))

    except Exception:
        logger.error("it's not rss format")
        sys.exit()

    make_dict = {}
    count = 0

    if not args.limit:
        args.limit = len(feed["items"])
    elif args.limit < 0:
        logger.error(f"negative limit is entered (You enter limit = {args.limit}) ")
        sys.exit()
    for item in feed["items"][:args.limit]:
        logger.info(f"Process item № {count + 1}")
        make_dict["Title"] = item['title']
        make_dict["PubDate"] = item['published']
        make_dict["Link"] = item["link"]
        data_ = list(make_dict.values())
        data.make_dataframe(data_)
        if args.date:
            pass
        elif args.json:
            print(json.dumps(make_dict, indent=3))
            count += 1
        else:
            for name_of_line, news in make_dict.items():
                print(f"{name_of_line}: {news}")
                count += 1


def main():
    args = create_parser(sys.argv[1:])
    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.date:
        if len(args.date) == 8 and int(args.date):
            data.make_csv()
            data.print_data(args.date, args.limit, args.verbose)
        else:
            logger.error(f"Bad date format")
            sys.exit()
    else:
        print_news(args)
        data.make_csv()

if __name__ == "__main__":
    main()
