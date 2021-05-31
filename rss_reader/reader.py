import cl_parser as psr
from feed_container import FeedContainer
import app_logger

import logging

logger = app_logger.get_logger(__name__)


def main():
    parser = psr.args_Parser()

    # verbose check
    if parser.args_Space.verbose:
        logger.handlers[1].setLevel("INFO")

    feed = FeedContainer(url=parser.args_Space.source)

    feed.print_feed_Info()
    feed.print_news(parser.args_Space.limit)

    if parser.args_Space.json:
        feed.save_as_json(parser.args_Space.limit)


if __name__ == '__main__':
    main()