import argparse
import json
import logging
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as Et
from datetime import datetime

from rss_reader.rss_reader import cache

VERSION = "2.0"


def valid_date(date_in_str):
    try:
        return datetime.strptime(date_in_str, "%Y%m%d")
    except ValueError:
        msg = f"Not a valid date: '{date_in_str}'."
        raise argparse.ArgumentTypeError(msg)


def build_args(args):
    """This function builds parser-object with command line args and return this object"""
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"Version {VERSION}",
        help="Print version info",
    )
    parser.add_argument(
        "source", nargs="?" if "--date" in args else None, type=str, help="RSS URL"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Outputs verbose status messages"
    )
    parser.add_argument(
        "--json", action="store_true", help="Print result as JSON in stdout"
    )
    parser.add_argument(
        "--limit", type=int, help="Limit news topics if this parameter provided"
    )
    parser.add_argument(
        "--date",
        type=valid_date,
        help="Print news from local cache for specified date",
    )

    return parser.parse_args(args[1:])


def get_response(link):
    """Function knocks on the link and returns response"""
    try:
        logging.info(f"Connection to {link} ...")
        response = urllib.request.urlopen(link)
    except (urllib.error.URLError, ValueError):
        logging.error(f"Connection to {link} failed. Does your URL correct?")
        sys.exit()

    return response


def parse_response(xml):
    """This function provides parse of xml with help of xml.etree.ElementTree: receive xml parameter
    and returns list of news"""
    tree = None
    try:
        tree = Et.parse(xml)
    except Et.ParseError:
        logging.error("Error occurred during parsing the document")
        sys.exit()
    root = tree.getroot()
    news_list = []
    channel = root.findtext("channel/title")
    for item in root.iter("item"):
        news_list.append(
            {
                "Feed": channel,
                "Title": item.findtext("title"),
                "Date": item.findtext("pubDate"),
                "Link": item.findtext("link"),
            }
        )
    return news_list


def calculate_news_with_limit(news_list, limit):
    if not limit:
        limit = len(news_list)
    return news_list[:limit]


def print_news(news_list):
    """Function prints news in stdout"""
    for item in news_list:
        print(
            f'Feed: {item.get("Feed")}',
            f'Title: {item.get("Title")}',
            f'Date: {item.get("Date")}',
            f'Link: {item.get("Link")}',
            "....................",
            sep="\n",
        )


def print_json(news_list):
    """Function prints news in json format"""
    print(json.dumps(news_list, indent=2, ensure_ascii=False))


def main(argv=sys.argv):
    """This function is entry point.Parser arguments are processed and checked here and in accordance with this,
    output format is selected"""
    parser_args = build_args(argv)
    if parser_args.verbose:
        logging.basicConfig(level=logging.INFO)
    limit = None
    if parser_args.limit is not None:
        limit = parser_args.limit
        if limit == 0 or limit < 0:
            logging.error("Limit is incorrect")
            sys.exit()
    local_storage = cache.Cache(logging)
    if parser_args.date:
        logging.info("Trying to get data from cache...")
        news_list = local_storage.get_news_by_date(parser_args.date, parser_args.source)
    else:
        logging.info("Trying to get data from source...")
        response = get_response(parser_args.source)
        if not response:
            logging.info("No data for requested URL")
            sys.exit()
        news_list = parse_response(response)
        local_storage.write_news(parser_args.source, news_list)
    news_list = calculate_news_with_limit(news_list, limit)
    if parser_args.json:
        print_json(news_list)
    else:
        print_news(news_list)

    logging.info("Data is received")


if __name__ == "__main__":
    main()
