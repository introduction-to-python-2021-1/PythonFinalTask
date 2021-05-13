import argparse
import sys
import logging
import json

import feedparser

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def create_parser(args):
    """create positional and optional arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 2.0")
    parser.add_argument("url", type=str, help="URL ")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")

    return parser.parse_args(args)


def open_url(url):
    """ try to open url """
    try:
        logger.info(f"open {url} and start parse")
        feed = feedparser.parse(url)
    except SystemExit:
        logger.error(f"cant open {url}")
        sys.exit()

    return feed


def print_news(args):
    """Check format and print news on console or json"""
    feed = open_url(args.url)
    try:
        if not args.json:
            print(f'Feed: {feed["channel"]["title"]}')
        else:
            print("JSON")
            with open("data_file.json", "w") as f:
                json.dump(feed["channel"]["title"], f, indent=3)

    except SystemExit:
        logger.error(f"it's not rss format")
        sys.exit()

    make_dict = {}
    count = 0

    for item in feed["items"][:args.limit]:
        logger.info(f"Process item № {count + 1}")
        make_dict["Title"] = item['title']
        make_dict["PubDate"] = item['published']
        make_dict["Link"] = item["link"]
        if args.json:
            with open("data_file.json", "a") as f:
                json.dump(make_dict, f, indent=3)
                count += 1

        else:

            for name_of_line, news in make_dict.items():
                print(f"{name_of_line}: {news}")
            count += 1


def main():
    args = create_parser(sys.argv[1:])
    if args.verbose:
        logger.setLevel(logging.INFO)
    print_news(args)


if __name__ == "__main__":
    main()
