import sys
import json
import logging
import argparse
from pathlib import Path
from itertools import islice
from urllib.request import urlopen
import xml.etree.ElementTree as ET

VERSION = "2.0"

logging.basicConfig(level=logging.ERROR, format="%(message)s")
logger = logging.getLogger()


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

    except Exception as e:
        logger.error("Couldn't get good response")
        sys.exit()

    return response


def process_response(response, limit):
    """
    Returns dictionary with channel title and items. Items number is determined by provided limit argument.

            Parameters:
                    response (http.client.HTTPResponse): Response from server provided by get_response function
                    limit (None) or (int): Max number of items in result dictionary

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

    for number_of_news_item, news_item in enumerate(
        islice(root.iterfind("channel/item"), 0, max(0, limit) if limit is not None else limit)
    ):

        logger.info(f"Process item № {number_of_news_item + 1}")

        channel_items.append({
            "Title": news_item.findtext("title"),
            "Date": news_item.findtext("pubDate"),
            "Link": news_item.findtext("link"),
        })

    return {"Title": root.findtext("channel/title"), "Items": channel_items}


def print_news(channel):
    """
    Prints news to console.

            Parameters:
                    {"Title": (str), "Items": (list)}: Dictionary with channel title and items
            Returns:
                    (None)
    """
    logger.info(f"Print news")

    print(f"\nFeed: {channel['Title']}")

    for news_item in channel["Items"]:
        print(f"\nTitle: {news_item['Title']}")
        print(f"Date: {news_item['Date']}")
        print(f"Link: {news_item['Link']}")


def write_json(channel):
    """
    Write news into data.json file in directory named data.

            Parameters:
                    {"Title": (str), "Items": (list)}: Dictionary with channel title and items
            Returns:
                    (None)
    """
    logger.info(f"Write json")

    base = Path(__file__).resolve().parent.parent / "data"
    jsonpath = base / "news.json"
    base.mkdir(exist_ok=True)
    jsonpath.write_text(json.dumps(channel, indent=4))


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("--version", action="version", version=f'"Version {VERSION}"', help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")

    args = parser.parse_args(argv[1:])

    if args.verbose:
        logger.setLevel(logging.INFO)

    response = get_response(args.source)
    channel_info_and_items = process_response(response, args.limit)
    print_news(channel_info_and_items)

    if args.json:
        write_json(channel_info_and_items)


if __name__ == "__main__":
    main()
