import logging
import sys

from src.modules.argparser import arg_parser
from src.modules.localcache import Cache
from src.modules.output import DefaultOutput, JSONOutput
from src.modules.rss_parser import RSSParser
from src.modules.url_validator import RssUrlManager

__version__ = 1.3


def create_logger() -> logging.getLogger:
    """ Function for creating logger object. """
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger()
    return logger


def main(argv=None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    logger = create_logger()

    parser = arg_parser().parse_args(args=argv)
    if parser.verbose:
        logger.setLevel(logging.DEBUG)
    logger.info('Started main')

    limit = parser.limit if parser.limit else 0

    output_data = None

    if parser.version:
        print(f'Version is {__version__}')
        logger.info('Main ended successfully')
    else:
        if parser.date:
            output_data = Cache(logger, parser.date, parser.source).get_from_cached_news()
        else:
            validator = RssUrlManager(parser.source, logger)
            url = validator.get_validated_url()
            rss_channel = validator.get_rss_from_url()
            if url and rss_channel:
                parsed_feed = RSSParser(rss_channel, logger).parse()
                output_data = parsed_feed
                logger.info('Main ended successfully')
            else:
                logger.info('Main ended unsuccessfully')

        if parser.json:
            handler = JSONOutput(limit)
            handler.output(*output_data) if parser.date else handler.output(output_data)
        else:
            handler = DefaultOutput(limit)
            handler.output(*output_data) if parser.date else handler.output(output_data)


if __name__ == '__main__':
    main()
