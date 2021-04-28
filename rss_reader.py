#!/usr/bin/env python
import sys
import json
import logging
import argparse
from itertools import islice
from urllib.request import urlopen
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_response(url):
    """Returns HTTPResponse from server using provided url."""
    global logger

    try:
        logger.info(f"Try to get response from: {url}")

        response = urlopen(url)

        if response.status != 200:
            raise Exception("Bad response")

    except Exception as e:
        logger.error(e)
        sys.exit()

    return response


def process_response(response, limit):
    """Returns dictionary with channel info and items. Items number is determined by provided limit argument."""
    global logger

    try:
        logger.info(f"Try to parse response: {response}")

        xmldoc = ET.parse(response)
        root = xmldoc.getroot()

        if root.tag != "rss":
            raise Exception("The document isn't RSS feed.")

    except Exception as e:
        logger.error(e)
        sys.exit()

    channel_title = root.findtext("channel/title")
    channel_items = []

    for i, item in enumerate(islice(root.iterfind("channel/item"), 0, max(0, limit) if limit is not None else limit)):
        logger.info(f"Process item № {i + 1}")

        channel_items.append({
            "Title": item.findtext("title"),
            "Date": item.findtext("pubDate"),
            "Link": item.findtext("link"),
        })

    return {"Title": root.findtext("channel/title"), "Items": channel_items}


def print_news(channel):
    """Prints news to console."""
    print(f"Feed: {channel['Title']}")

    for item in channel["Items"]:
        print("")
        for key, value in item.items():
            print(f"{key}: {value}")


def main(argv):
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")

    args = parser.parse_args(argv[1:])

    if not args.verbose:
        logger.disabled = True

    response = get_response(args.source)
    channel_info_and_items = process_response(response, args.limit)
    print_news(channel_info_and_items)

    if args.json:
        with open("data.json", "w") as f:
            json.dump(channel_info_and_items, f, indent=4)


if __name__ == "__main__":
    main(sys.argv)
