import logging

from src.modules.argparser import arg_parser
from src.modules.output import DefaultOutput, JSONOutput
from src.modules.rss_parser import RSSParser
from src.modules.url_validator import RssUrlValidator

__version__ = 1.0


def create_logger() -> logging.getLogger:
    """FUNCTION FOR CREATING LOGGER OBJECT"""
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger()
    return logger


def main() -> None:
    logger = create_logger()

    parser = arg_parser().parse_args()

    if parser.verbose:
        logger.setLevel(logging.DEBUG)
    logger.info('Started main')

    if parser.limit:
        limit = parser.limit
    else:
        limit = 0

    url = RssUrlValidator(parser.source, logger).get_validated_url()
    if parser.version:
        print(f'Version is {__version__}')
    elif url:
        if parser.json:
            handler = JSONOutput()
            handler.output(RSSParser(url, logger, limit).parse())
        else:
            handler = DefaultOutput()
            handler.output(RSSParser(url, logger, limit).parse())
        logger.info('Main ended successfully')
    else:
        logger.info('Main ended unsuccessfully')


if __name__ == '__main__':
    main()
