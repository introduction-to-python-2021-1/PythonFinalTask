"""
    RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format
"""
import argparse
import json
import sys

from rss_core.cacher import DbCacher
from rss_core.converter import RssConverter
from rss_core.news_processor import NewsProcessor
from rss_core.parser import XmlParser
from rss_core.reader import SiteReader
from utils import util

__version__ = "1.4"
RSS_DB = "data/rss_news_bd.db"


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    arg_parser = init_arg_parser()
    my_args = arg_parser.parse_args(argv)
    news_limit = my_args.limit
    if news_limit is not None and news_limit <= 0:
        util.log(show_on_console=True, flag="ERROR", msg=f"[ERROR] Limit should be positive integer")
        exit(1)

    try:
        parser = XmlParser(reader=SiteReader())
        cacher = DbCacher(RSS_DB)
        rss_converter = RssConverter()
        news_processor = NewsProcessor(parser=parser, cacher=cacher, converter=rss_converter, show_logs=my_args.verbose)
        if my_args.date:
            news_processor.restore_news_from_cache(my_args.date, my_args.source)
        elif my_args.source:
            news_processor.load_news(my_args.source)
        else:
            util.log(show_on_console=True, flag="ERROR",
                     msg=f"Please, enter source or --date for correct work of rss_reader")
            exit(1)

        if my_args.json:
            print(json.dumps(news_processor.get_news_as_json(news_limit), indent=4, ensure_ascii=False))
        else:
            print(news_processor.get_news_as_str(news_limit))

        if my_args.to_html:
            news_processor.save_news_as_html(my_args.to_html, news_limit)
        if my_args.to_pdf:
            news_processor.save_news_as_pdf(my_args.to_pdf, news_limit)


    except Exception as err:
        util.log(show_on_console=True, flag="ERROR", msg=f"Unexpected error has occurred: {str(err)}")


def init_arg_parser():
    """
    Initialize parser
    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', nargs='?', type=str, default=None, help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + __version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', default=None, type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', default=None, type=str, help='Publishing date for restoring news from cache')
    parser.add_argument('--to-html', default=None, type=str, help='Save news to html file')
    parser.add_argument('--to-pdf', default=None, type=str, help='Save news to pdf file')
    return parser


if __name__ == "__main__":
    main(["--to-html", "a.html", "https://news.yahoo.com/rss/"])
