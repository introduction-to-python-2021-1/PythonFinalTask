import sys
import json
import logging
import argparse
from pathlib import Path
from itertools import islice
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

try:
    from local_storage import LocalStorage
    from logger_config import get_logger
except ImportError:
    from .local_storage import LocalStorage
    from .logger_config import get_logger

VERSION = "2.0"

local_storage = LocalStorage("localstorage")
logger = get_logger()


def get_response(url):
    """
    Returns HTTPResponse from server using provided url.

            Parameters:
                    url (str): URL to RSS feed content

            Returns:
                    response (http.client.HTTPResponse): Response from server
    """
    try:
        logger.info(f"Get response from: {url}")

        response = urlopen(url)

    except HTTPError as e:
        logger.error(f"The server couldn't fulfill the request.\nError code: {e.code}")
        sys.exit()
    except URLError as e:
        logger.error(f"Failed to reach a server.\nReason: {e.reason}")
        sys.exit()
    except Exception as e:
        logger.error(f"Generic exception: {e}")
        sys.exit()

    return response


def parse_response(response):
    """
    Returns list with news items.

            Parameters:
                    response (http.client.HTTPResponse): Response from server provided by get_response function

            Returns:
                    [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str)}]: List of dictionaries
    """
    try:
        logger.info(f"Parse response")

        xmldoc = ET.parse(response)
        root = xmldoc.getroot()

        if root.tag != "rss":
            raise Exception("The document isn't RSS feed")

    except Exception as e:
        logger.error("Couldn't parse response")
        sys.exit()

    channel_title = root.findtext("channel/title")
    news_items = []

    for index_of_news_item, news_item in enumerate(root.iterfind("channel/item")):
        logger.info(f"Process item № {index_of_news_item + 1}")

        news_items.append({
            "Feed": channel_title,
            "Title": news_item.findtext("title"),
            "Date": news_item.findtext("pubDate"),
            "Link": news_item.findtext("link"),
        })

    return news_items


def limit_news_items(news_items, limit):
    """
    Returns limited list with news items. Items number is determined by provided limit argument.

            Parameters:
                    news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str)}]: List of dictionaries
                    limit (None) or (int): Max number of items in result dictionary, if (None) all items are included

            Returns:
                    [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str)}]: Limited list of dictionaries
    """
    calculated_limit = max(0, limit) if limit is not None else limit

    if limit != calculated_limit:
        logger.warning(f"You provided wrong --limit argument, your limit set to {calculated_limit}")
    else:
        logger.info(f"Limit output to {calculated_limit} news items")

    return news_items[:calculated_limit]


def print_news(news_items):
    """
    Prints news to stdout.

            Parameters:
                    news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str)}]: List of dictionaries
    """
    logger.info(f"Print news items")

    for news_item in news_items:
        print()
        print(f"Feed: {news_item['Feed']}")
        print(f"Title: {news_item['Title']}")
        print(f"Date: {news_item['Date']}")
        print(f"Link: {news_item['Link']}")


def print_json(news_items):
    """
    Prints news as JSON in stdout.

            Parameters:
                    news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str)}]: List of dictionaries
    """
    logger.info(f"Print news items as JSON")

    print(json.dumps(news_items, indent=4, ensure_ascii=False))


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    # If you read the string down below, please don't copy it, I worked too hard on it ;-)
    parser.add_argument("source", nargs="?" if "--date" in argv else None, type=str, help="RSS URL")
    parser.add_argument("--version", action="version", version=f'"Version {VERSION}"', help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=str, help="Return news topics which were published in specific date")

    args = parser.parse_args(argv[1:])

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.date:

        if args.source:
            news_items = local_storage.get_channel_by_url_and_date(args.source, args.date)
        else:
            news_items = local_storage.get_channel_by_url_and_date(None, args.date)

        if not news_items:
            logger.error("Couldn't find news topics which were published in specific date")
            sys.exit()

    else:
        response = get_response(args.source)
        news_items = parse_response(response)
        local_storage.set_channel_by_url(args.source, news_items)

    news_items = limit_news_items(news_items, args.limit)
    print_news(news_items)

    if args.json:
        print_json(news_items)


if __name__ == "__main__":
    main()
