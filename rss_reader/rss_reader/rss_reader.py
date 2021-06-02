import argparse
import json
import logging
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as Et

VERSION = "2.0"


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


def print_news(news, limit):
    """Function prints news in stdout"""
    for item in news[:limit]:
        print(
            f'Feed: {item.get("Feed")}',
            f'Title: {item.get("Title")}',
            f'Date: {item.get("Date")}',
            f'Link: {item.get("Link")}',
            "....................",
            sep="\n",
        )


def print_json(news_list, limit):
    if not limit:
        limit = len(news_list)
    """Function prints news in json format"""
    print(json.dumps(news_list[:limit], indent=2, ensure_ascii=False))


def main():
    """This function is entry point.Parser arguments are processed and checked here and in accordance with this,
    output format is selected"""
    parser_args = build_args(sys.argv[1:])
    if parser_args.verbose:
        logging.basicConfig(level=logging.INFO)
    limit = None
    if parser_args.limit is not None:
        limit = parser_args.limit
        if limit == 0 or limit < 0:
            logging.error("Limit is incorrect")
            sys.exit()
    logging.info("Trying to get data...")
    response = get_response(parser_args.source)
    if not response:
        logging.info("No data for requested URL")
        sys.exit()
    news_list = parse_response(response)
    if parser_args.json:
        print_json(news_list, limit)
    else:
        print_news(news_list, limit)

    logging.info("Data is received")


if __name__ == "__main__":
    main()
