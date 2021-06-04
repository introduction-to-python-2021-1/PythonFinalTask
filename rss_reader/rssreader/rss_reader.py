"""
    RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format
"""
import argparse
import json
import sys

from rss_core.cacher import DbCacher
from rss_core.news_processor import NewsProcessor
from rss_core.parser import XmlParser
from rss_core.reader import SiteReader
from utils import util

__version__ = "1.4"
RSS_DB = "data/rss_news_db.db"


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    arg_parser = init_arg_parser()
    given_arguments = arg_parser.parse_args(argv)
    news_limit = given_arguments.limit
    if news_limit is not None and news_limit <= 0:
        util.log(show_on_console=True, flag="ERROR", msg=f"[ERROR] Limit should be positive integer")
        exit(1)

    try:
        parser = XmlParser(reader=SiteReader())
        cacher = DbCacher(RSS_DB)
        news_processor = NewsProcessor(parser=parser, cacher=cacher, show_logs=given_arguments.verbose)
        if given_arguments.date:
            news_processor.restore_news_from_cache(given_arguments.date, given_arguments.source)
        elif given_arguments.source:
            news_processor.load_news(given_arguments.source)
        else:
            util.log(show_on_console=True, flag="ERROR",
                     msg=f"Please, enter source or --date for correct work of rss_reader")
            exit(1)

        if given_arguments.json:
            print(json.dumps(news_processor.get_news_as_json(news_limit), indent=4, ensure_ascii=False))
        else:
            print(news_processor.get_news_as_str(news_limit))

        if given_arguments.to_html is not None:
            if given_arguments.to_html:
                news_processor.save_news_as_html(given_arguments.to_html, news_limit)
            else:
                print("Please, choose dir or filename fro convening to html")
        if given_arguments.to_pdf is not None:
            if given_arguments.to_pdf:
                news_processor.save_news_as_pdf(given_arguments.to_pdf, news_limit)
            else:
                print("Please, choose dir or filename fro convening to pdf")

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
    main(["https://www.yahoo.com/news/rss", "--limit", "1", "--verbose", "--to-html", "",
          "--to-pdf", ""])
