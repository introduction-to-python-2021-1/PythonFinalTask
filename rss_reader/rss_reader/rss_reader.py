import argparse
import sys
import xml.etree.ElementTree as Et
import urllib.request
import urllib.error
import logging
import json

VERSION = "1.0"


def build_args(args):
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

    return parser.parse_args(args)


def get_response(link):
    """Function knocks on the link nad returns response"""
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
    try:
        for item in news[:limit]:
            print(
                f'Feed: {item["Feed"]}',
                f'Title: {item["Title"]}',
                f'Date: {item["Date"]}',
                f'Link: {item["Link"]}',
                "....................",
                sep="\n",
            )
    except KeyError:
        logging.error("Error during printing news. Possible problem in xml structure")


def print_json(news, limit):
    """Function prints news in json format"""
    print(json.dumps(news[:limit], indent=2, ensure_ascii=False))


def main():
    """This function is entry point.Parser arguments are processed and checked here and in accordance with this,
    output format is selected"""
    args = build_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    limit = args.limit
    # if limit == 0 or limit < 0:
    #     logging.error("Limit is incorrect")
    #     sys.exit()
    response = get_response(args.source)
    if not response:
        logging.info("No data for requested URL")
        sys.exit()
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
