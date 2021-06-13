import logging
import sys

from src.modules.argparser import arg_parser
from src.modules.output import DefaultOutput, JSONOutput
from src.modules.rss_parser import RSSParser
from src.modules.url_validator import RssUrlValidator

__version__ = 2.0


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

    if parser.version:
        print(f'Version is {__version__}')
        logger.info('Main ended successfully')
    else:
        url = RssUrlValidator(parser.source, logger).get_validated_url()
        if url:
            if parser.json:
                parsed_feed = RSSParser(url, logger, limit).parse()
                handler = JSONOutput()
                print(handler.output(parsed_feed))
            else:
                parsed_feed = RSSParser(url, logger, limit).parse()
                handler = DefaultOutput()
                print(handler.output(parsed_feed))
            logger.info('Main ended successfully')
        else:
            logger.info('Main ended unsuccessfully')


if __name__ == '__main__':
    main()
