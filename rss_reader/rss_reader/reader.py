import rss_reader.cl_parser as cl_parser
import rss_reader.feed_container as feed_container
import rss_reader.app_logger as app_logger


logger = app_logger.get_logger(__name__)

def main():
    parser = cl_parser.args_Parser()

    # verbose check
    if parser.args_Space.verbose:
        logger.handlers[1].setLevel("INFO")

    feed = feed_container.FeedContainer(url=parser.args_Space.source)

    feed.print_feed_Info()
    feed.print_news(parser.args_Space.limit)

    if parser.args_Space.json:
        feed.save_as_json(parser.args_Space.limit)


if __name__ == '__main__':
    main()