import os
import argparse
import sys
import logging
import json
from urllib.error import URLError
from rss_reader.dataset import Data

import feedparser

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


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
    """
    Try to open url

    Parameter
        url page
    Return
        feed of news
    """

    try:
        logger.info(f"open {url} and start parse")
        feed = feedparser.parse(url)
        logger.info(f"{feed['channel']['title']}")
    except URLError:
        logger.error(f"cant open or found {url}")
        sys.exit()
    except SystemExit:
        logger.error(f"exception: {Exception}")
        sys.exit()
    except Exception:
        logger.error("Not rss format")
        sys.exit()
    return feed


def parse_news(args, data):
    """
    Parse news

    Parameter:
            args from the user(url, verbose, limit, json)
    """
    feed = open_url(args.url)

    if not args.json:
        print(f'Feed: {feed["channel"]["title"]}')
    else:
        print(json.dumps(feed["channel"]["title"], indent=3))

    count = 0

    if args.limit is None:
        args.limit = len(feed["items"])
    elif args.limit <= 0:
        logger.error(f"limit is entered (You enter limit = {args.limit}) ")
        sys.exit()

    for item in feed["items"][:args.limit]:
        logger.info(f"Process item № {count + 1}")
        count += 1
        feed_news = dict()
        feed_news["Title"] = item['title']
        feed_news["Date"] = item['published']
        feed_news["Link"] = item["link"]
        data.append_dataframe(feed_news)
        if not args.date:
            print_news(args, feed_news)


def print_news(args, feed_news):
    """
    Print news

    Parameter:
            args from the user(url, verbose, limit, json)
            feed_news = news
    """
    if args.date:
        for date, title, link in zip(feed_news['Date'], feed_news['Title'], feed_news['Link']):
            if args.json:
                patch_data = dict()
                patch_data["Title"] = title
                patch_data["Date"] = date
                patch_data["Link"] = link
                print(json.dumps(patch_data, indent=3))
            else:
                print(f"Title :{title}")
                print(f"Date : {date}")
                print(f"Link : {link}\n")

    elif args.json:

        print(json.dumps(feed_news, indent=3))

    else:
        for name_of_line, news in feed_news.items():
            print(f"{name_of_line}: {news}")


def main():
    args = create_parser(sys.argv[1:])
    data = Data()

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.url:
        parse_news(args, data)
    data.append_cache()

    if args.date:
        if len(args.date) == 8 and int(args.date) and int(args.date) > 20210500:
            news = data.sort_data(args.date, args.limit, args.verbose)
            print_news(args, news)

        else:
            logger.error(f"Bad date format")
            sys.exit()


if __name__ == "__main__":
    main()
