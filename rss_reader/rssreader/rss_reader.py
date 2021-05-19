"""
    RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format
"""
import argparse

__version__ = "1.2"

from rssreader.rss_core.news_processor import NewsProcessor
from rssreader.rss_core.parser import XMLParser
from rssreader.rss_core.reader import SiteReader
from rssreader.utils import util


def main():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', help='RSS URL')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', default=None, help='Limit news topics if this parameter provided')
    my_args = parser.parse_args()
    news_limit = None
    try:
        news_limit = int(my_args.limit) if isinstance(my_args.limit, str) else my_args.limit
    except ValueError:
        util.log(show_on_console=True, flag="ERROR", msg=f"Invalid value for --limit. Use int>0")
        exit()

    try:
        parser = XMLParser(reader=SiteReader())
        news_processor = NewsProcessor(parser=parser, show_logs=my_args.verbose)
        rss_news = news_processor.get_news(my_args.source, news_limit)
        if my_args.json:
            print(rss_news.as_json())
        else:
            print(rss_news)
    except Exception as err:
        util.log(show_on_console=True, flag="ERROR", msg=f"Unexpected error has occurred {err.__class__}: {str(err)}")


if __name__ == "__main__":
    main()
