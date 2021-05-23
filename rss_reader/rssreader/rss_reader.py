"""
    RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format
"""
__version__ = "1.2"

import argparse
import sys

from rss_core.news_processor import NewsProcessor
from rss_core.parser import XmlParser
from rss_core.reader import SiteReader
from utils import util


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    my_args = get_args(argv)
    news_limit = None
    try:
        news_limit = int(my_args.limit) if isinstance(my_args.limit, str) else my_args.limit
    except ValueError:
        util.log(show_on_console=True, flag="ERROR", msg=f"Invalid value for 'limit'. Expected integer>0")
        exit(1)

    try:
        parser = XmlParser(reader=SiteReader())
        news_processor = NewsProcessor(parser=parser, show_logs=my_args.verbose)
        rss_news = news_processor.get_news(my_args.source)
        if my_args.json:
            print(rss_news.as_json(limit=news_limit))
        else:
            print(rss_news.as_str(limit=news_limit))
    except Exception as err:
        util.log(show_on_console=True, flag="ERROR", msg=f"Unexpected error has occurred: {str(err)}")


def get_args(argv):
    """
    Initialize arg parser and parse argv
    :param argv: input arguments
    :return: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + __version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', default=None, help='Limit news topics if this parameter provided')
    return parser.parse_args(argv)


if __name__ == "__main__":
    main()
