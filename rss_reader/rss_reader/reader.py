import sys

import rss_reader.cl_parser as cl_parser
import rss_reader.feed_container as feed_container
import rss_reader.app_logger as app_logger
import rss_reader.local_storage as local_storage

logger = app_logger.get_logger(__name__)


def main():
    # command line arguments parse
    parser = cl_parser.args_parser()

    # Various combinations of parameters command line.
    if parser.args_Space.source:
        feed = feed_container.FeedContainer(url=parser.args_Space.source)
        feed.save_as_json()

        feed.print_feed_Info()

        if parser.args_Space.json and parser.args_Space.date:
            feed.print_news_by_date_json_format(parser.args_Space.date, parser.args_Space.limit)
        elif parser.args_Space.date:
            feed.print_news_by_date(parser.args_Space.date, parser.args_Space.limit)
        else:
            if parser.args_Space.json:
                feed.print_news_json_format(parser.args_Space.limit)
            else:
                feed.print_news(parser.args_Space.limit)
    elif parser.args_Space.date:
        local_feed = local_storage.local_storage()
        if parser.args_Space.json:
            local_feed.print_news_from_storage_by_date_json_format(parser.args_Space.date)
        else:
            local_feed.print_news_from_storage_by_date(parser.args_Space.date)

    else:
        logger.error("No attributes <source> or <date>. Check --help")
        sys.exit


if __name__ == '__main__':
    main()
