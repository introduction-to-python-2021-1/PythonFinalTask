import sys

import rss_reader.cl_parser as cl_parser
import rss_reader.feed_container as feed_container
import rss_reader.app_logger as app_logger
import rss_reader.local_storage as local_storage

logger = app_logger.get_logger(__name__)


def main(argv=sys.argv[1:]):
    # command line arguments parse
    parser = cl_parser.args_parser(argv)

    # if command line arguments have a link
    if parser.args_Space.source:

        # create feed container
        feed = feed_container.FeedContainer(url=parser.args_Space.source)

        # save local storage, format 'a" append
        feed.save_as_json()

        # print feed info
        feed.print_feed_Info()

        # print news
        feed.print_news_by_args(date=parser.args_Space.date,
                                limit=parser.args_Space.limit,
                                json=parser.args_Space.json)
    elif parser.args_Space.date:
        pass


if __name__ == '__main__':
    main()
