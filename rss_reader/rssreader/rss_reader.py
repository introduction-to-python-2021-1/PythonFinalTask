"""
    RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format
"""
import argparse
import sys
from rss_core.cacher import DbCacher
from rss_core.news_processor import NewsProcessor
from rss_core.parser import XmlParser
from rss_core.reader import SiteReader
from utils import util

__version__ = "1.3"
RSS_DB = "data/rss_news_bd.db"


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    arg_parser = init_arg_parser()
    my_args = arg_parser.parse_args(argv)
    news_limit = None
    try:
        news_limit = int(my_args.limit) if isinstance(my_args.limit, str) else my_args.limit
    except ValueError:
        util.log(show_on_console=True, flag="ERROR", msg=f"Invalid value for 'limit'. Expected integer>0")
        exit(1)

    try:
        parser = XmlParser(reader=SiteReader())
        cacher = DbCacher(RSS_DB)
        news_processor = NewsProcessor(parser=parser, cacher=cacher, show_logs=my_args.verbose)
        if my_args.date:
            rss_news = news_processor.cacher.get_from_cache(my_args.source, my_args.date, show_logs=my_args.verbose)
        else:
            rss_news = news_processor.get_news(my_args.source, cache_is_on=True)
        if my_args.json:
            print(rss_news.as_json(limit=news_limit))
        else:
            print(rss_news.as_str(limit=news_limit))

    except Exception as err:
        util.log(show_on_console=True, flag="ERROR", msg=f"Unexpected error has occurred: {str(err)}")


def init_arg_parser():
    """
    Initialize parser
    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + __version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', default=None, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', default=None, help='Publishing date for restoring news from cache')
    return parser


if __name__ == "__main__":
    main()
