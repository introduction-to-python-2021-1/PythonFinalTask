import rss_reader.cl_parser as cl_parser
import rss_reader.feed_container as feed_container
import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)


def main():
    parser = cl_parser.args_parser()

    feed = feed_container.FeedContainer(url=parser.args_Space.source)

    feed.print_feed_Info()

    # This block of code prints news depending on the parameters
    # --date and --limit
    if parser.args_Space.date:
        feed.print_news_by_date(parser.args_Space.date, parser.args_Space.limit)
    else:
        feed.print_news(parser.args_Space.limit)

    # This block of code save news as json depending on the parameters
    # --json --date -- limit
    if parser.args_Space.json and parser.args_Space.date:
        feed.save_as_json_by_date(parser.args_Space.date, parser.args_Space.limit)
    elif parser.args_Space.json :
        feed.save_as_json(parser.args_Space.limit)


if __name__ == '__main__':
    main()
