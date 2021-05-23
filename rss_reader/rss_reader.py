import argparse
import xml.etree.ElementTree as Et
import urllib.request
import urllib.error
import logging
import json

VERSION = "1.0"


def build_args():
    """This function builds parser-object with command line args and return this object"""
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"Version {VERSION}",
        help="Print version info",
    )
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument(
        "--verbose", action="store_true", help="Outputs verbose status messages"
    )
    parser.add_argument(
        "--json", action="store_true", help="Print result as JSON in stdout"
    )
    parser.add_argument(
        "--limit", type=int, help="Limit news topics if this parameter provided"
    )

    return parser.parse_args()


def get_response(link):
    """Function knocks on the link nad returns response"""
    response = None
    try:
        logging.info(f"Connection to {link} ...")
        response = urllib.request.urlopen(link)
    except (urllib.error.URLError, ValueError):
        logging.error(f"Connection to {link} failed. Does your URL correct?")
        exit()

    return response


def parse_response(xml):
    """This function provides parse of xml with help of xml.etree.ElementTree: receive xml parameter
    and returns list of news"""
    tree = Et.parse(xml)
    root = tree.getroot()
    news = []
    channel = root.findtext("channel/title")
    for item in root.iter("item"):
        news.append(
            {
                "Feed": channel,
                "Title": item.findtext("title"),
                "Date": item.findtext("pubDate"),
                "Link": item.findtext("link"),
            }
        )
    return news


def print_news(news, limit):
    """Function prints news in stdout"""
    for item in news[:limit]:
        print(
            f'Feed: {item["Feed"]}',
            f'Title: {item["Title"]}',
            f'Date: {item["Date"]}',
            f'Link: {item["Link"]}',
            "....................",
            sep="\n",
        )


def print_json(news, limit):
    """Function prints news in json format"""
    print(json.dumps(news[:limit], indent=2, ensure_ascii=False))


def main():
    """This function is entry point.Parser arguments are processed and checked here and in accordance with this,
    output format is selected"""
    args = build_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    limit = args.limit
    if limit and limit <= 0:
        logging.error("Limit is incorrect")
        exit()
    response = get_response(args.source)
    if not response:
        logging.info("No data for requested URL")
        exit()
    logging.info("Trying to get data...")
    news = parse_response(response)
    if not limit:
        limit = len(news)
    if args.json:
        print_json(news, limit)
    else:
        print_news(news, limit)

    logging.info("Data is received")


if __name__ == "__main__":
    main()
