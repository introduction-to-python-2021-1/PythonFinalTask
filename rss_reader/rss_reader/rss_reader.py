import argparse
import json
import logging
import sys
import urllib.error
import urllib.request
from datetime import datetime

import feedparser
from pathvalidate.argparse import validate_filepath_arg

from rss_reader.rss_reader.converter import Converter
from rss_reader.rss_reader.local_storage import Cache

VERSION = "4.0"


def valid_date(date_in_str):
    """This function validate date: receives date in str and return datetime object or raise error"""
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
        help="Print news from local storage for specified date",
    )
    parser.add_argument(
        "--to-html", type=validate_filepath_arg, help="Converts news to HTML format"
    )
    parser.add_argument(
        "--to-pdf", type=validate_filepath_arg, help="Converts news to PDF format"
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
    content = feedparser.parse(xml)
    news_list = []
    channel = content.get("channel").get("title")
    for item in content.entries:
        news_list.append(
            {
                "Feed": channel,
                "Title": item.get("title"),
                "Date": item.get("published"),
                "Link": item.get("link"),
                "Image": item.get("media_content")[0].get("url")
                if item.get("media_content") is not None
                else None,
            }
        )
    return news_list


def calculate_news_with_limit(news_list, limit):
    """This function receives list of news and limit from user and returns slice"""
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
            f'Image: {item.get("Image")}',
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
    local_storage = Cache("storage", "storage.json", logging)
    if parser_args.date:
        logging.info("Trying to get data from storage...")
        news_list = local_storage.get_news_by_date(parser_args.date, parser_args.source)
    else:
        logging.info("Trying to get data from source...")
        response = get_response(parser_args.source)
        if not response:
            logging.info("No data for requested URL")
            sys.exit()
        news_list = parse_response(response)
        local_storage.write_news(parser_args.source, news_list)
        local_storage.save_images(news_list)
    news_list = calculate_news_with_limit(news_list, limit)
    if parser_args.json:
        print_json(news_list)
    else:
        print_news(news_list)

    logging.info("Data is received")

    if parser_args.to_html:
        converter = Converter(
            parser_args.to_html, f"news({datetime.now()}).html", logging
        )
        converter.convert_to_html(news_list)
    if parser_args.to_pdf:
        converter = Converter(
            parser_args.to_pdf, f"news({datetime.now()}).pdf", logging
        )
        converter.convert_to_pdf(news_list)


if __name__ == "__main__":
    main()
