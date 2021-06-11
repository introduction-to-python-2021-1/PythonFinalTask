import os
import argparse
import sys
import logging
import json
from urllib.error import URLError

from termcolor import cprint
import pandas as pd

from rss_reader.convert import Epub, HTML
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
    parser.add_argument("-d", "--date", type=str, help="Sort news for date")
    parser.add_argument("-e", "--to-epub", type=str, help="Converts news to Epub format", dest="to_epub")
    parser.add_argument("-s", "--to-html", type=str, help="Converts news to HTML format", dest="to_html")
    parser.add_argument("--colorize", action="store_true", help="color print")
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
    list_news = pd.DataFrame()
    for item in feed["items"]:
        count += 1
        logger.info(f"Process item № {count}")
        feed_news = dict()
        feed_news["Title"] = item['title']
        feed_news["Date"] = item['published']
        feed_news["Link"] = item["link"]
        if 'media_content' in item:
            feed_news["img"] = item.media_content[0]["url"]
        else:
            feed_news["img"] = None
        data.append_dataframe(feed_news)
        list_news = list_news.append(feed_news, ignore_index=True)
    return list_news[:args.limit]


def print_news(args, feed_news):
    """
    Print news

    Parameter:
            args from the user(url, verbose, limit, json)
            feed_news = news
    """
    if args.colorize:
        for date, title, link in zip(feed_news['Date'], feed_news['Title'], feed_news['Link']):
            if args.json:
                patch_data = dict()
                patch_data["Title"] = title
                patch_data["Date"] = date
                patch_data["Link"] = link
                cprint(json.dumps(patch_data, indent=3), "green", "on_magenta")
            else:
                cprint(f"Title : {title}", "yellow")
                cprint(f"Date : {date}", "grey", attrs=["blink"])
                cprint(f"Link : {link}\n", "cyan")
    else:
        for date, title, link in zip(feed_news['Date'], feed_news['Title'], feed_news['Link']):
            if args.json:
                patch_data = dict()
                patch_data["Title"] = title
                patch_data["Date"] = date
                patch_data["Link"] = link
                print(json.dumps(patch_data, indent=3))
            else:
                print(f"Title : {title}")
                print(f"Date : {date}")
                print(f"Link : {link}\n")


def convert(args):
    """Convert on epub or html format"""
    if not args.date:
        feed = pd.read_csv("data.csv")[:args.limit]
    else:
        data = Data()
        data.update_cache()
        feed = data.sort_data(args.date, args.limit, args.verbose)
    if args.to_html:
        try:
            file = HTML(feed)
            file.make_file(args.to_html)
        except FileNotFoundError as e:
            logger.error(f"{e} with way {args.to_html}")
            sys.exit()
    if args.to_epub:
        try:
            file = Epub()
            open(f"{args.to_epub}.txt")
            os.remove(f"{args.to_epub}.txt")
            file.make_file(feed, args.to_epub)
        except FileNotFoundError as e:
            logger.error(f"{e} with way {args.to_epub}")
            sys.exit()


def limit_checker(args):
    """Check limit"""
    if args.limit is None:
        args.limit = None
    elif args.limit <= 0:
        logger.error(f"The limit was entered incorrectly (You enter limit = {args.limit}) ")
        sys.exit()
    return args.limit


def date_checker(args):
    """Check date format"""
    if len(args.date) == 8 and int(args.date) and int(args.date) > 20210500:
        return args.date
    else:
        logger.error("Bad date format")
        if os.path.getsize("data.csv") == 1:
            os.remove("data.csv")
        sys.exit()


def main():
    args = create_parser(sys.argv[1:])
    limit_checker(args)
    data = Data()
    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.url:
        feed = parse_news(args, data)
        if not args.date:
            print_news(args, feed)
    data.update_cache()

    if args.date:
        date_checker(args)
        news = data.sort_data(args.date, args.limit, args.verbose)
        print_news(args, news)

    if args.to_html or args.to_epub:
        convert(args)


if __name__ == "__main__":
    main()
