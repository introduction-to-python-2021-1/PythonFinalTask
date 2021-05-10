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
except ImportError:
    from .local_storage import LocalStorage

VERSION = "2.0"

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logger = logging.getLogger()

local_storage = LocalStorage("localstorage")


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
    Returns dictionary with channel title and items.

            Parameters:
                    response (http.client.HTTPResponse): Response from server provided by get_response function

            Returns:
                    {"Title": (str), "Items": (list)}: Dictionary with channel title and items
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
    channel_items = []

    for index_of_news_item, news_item in enumerate(root.iterfind("channel/item")):
        logger.info(f"Process item № {index_of_news_item + 1}")

        channel_items.append({
            "Title": news_item.findtext("title"),
            "Date": news_item.findtext("pubDate"),
            "Link": news_item.findtext("link"),
        })

    return {"Title": root.findtext("channel/title"), "Items": channel_items}


def set_limit(channel, limit):
    """
    Returns dictionary with channel title and items. Items number is determined by provided limit argument.

            Parameters:
                    channel {"Title": (str), "Items": (list)}: Dictionary with channel title and items
                    limit (None) or (int): Max number of items in result dictionary, if (None) all items are included

            Returns:
                    {"Title": (str), "Items": (list)}: Dictionary with channel title and items
    """
    logger.info(f"Limit output")

    calculated_limit = max(0, limit) if limit is not None else limit
    if limit != calculated_limit:
        logger.warning(f"You provided wrong --limit argument , your limit set to {calculated_limit}")
    # Changes input dictionary "channel", not creates a copy of it
    channel["Items"] = channel["Items"][:calculated_limit]

    return channel


def print_news(channel):
    """
    Prints news to console.

            Parameters:
                    {"Title": (str), "Items": (list)}: Dictionary with channel title and items
    """
    logger.info(f"Print news")

    print(f"\nFeed: {channel['Title']}")

    for news_item in channel["Items"]:
        print(f"\nTitle: {news_item['Title']}")
        print(f"Date: {news_item['Date']}")
        print(f"Link: {news_item['Link']}")


def print_json(channel):
    """
    Print channel as JSON in stdout.

            Parameters:
                    {"Title": (str), "Items": (list)}: Dictionary with channel title and items
    """
    logger.info(f"Print channel as JSON in stdout")

    print(json.dumps(channel, sort_keys=False, indent=4))


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", type=str, help="RSS URL")
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
            channel_info_and_items = local_storage.get_channel_by_url_and_date(args.source, args.date)
        else:
            channel_info_and_items = local_storage.get_channel_by_url_and_date(None, args.date)

        if channel_info_and_items is None:
            logger.error("Couldn't find news topics which were published in specific date")
            sys.exit()

    else:
        response = get_response(args.source)
        channel_info_and_items = parse_response(response)
        local_storage.set_channel_by_url(args.source, channel_info_and_items)

    set_limit(channel_info_and_items, args.limit)
    print_news(channel_info_and_items)

    if args.json:
        print_json(channel_info_and_items)


if __name__ == "__main__":
    main()