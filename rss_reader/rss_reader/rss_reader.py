import logging
import sys

from modules.argparser import Argparser
from modules.cache import Cache
from modules.connector import Connector
from modules.output import ConsoleOutput
from modules.rssparser import RSSparser

VERSION = 2.1


def create_logger():
    """
    Logger creation
    :return: logger object
    """
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger()
    return logger


def main(argv=sys.argv):
    logger = create_logger()
    args = Argparser(logger=logger).parse_arguments(argv=argv[1:])

    if args['verbose']:
        logger.setLevel(logging.DEBUG)

    logger.info('Starting the program.')

    if args['version']:
        print('\nVersion {}'.format(VERSION))

    else:
        if args['date']:
            if args['source']:
                news = Cache(logger=logger).get_from_cache(date=args['date'], url=args['source'])
            else:
                news = Cache(logger=logger).get_from_cache(date=args['date'])

        else:
            if args['source']:
                connection = Connector(url=args['source'], logger=logger)
                if Connector(url=args['source'], logger=logger).is_connect:
                    news = RSSparser(source=connection.response_text,
                                     url=connection.url,
                                     logger=logger
                                     ).parse_news()
        if news:
            with ConsoleOutput(logger=logger) as console:
                if args['json']:
                    console.output_json(data=news, limit=args['limit'])
                else:
                    console.output(data=news, limit=args['limit'])

    logger.info('Termination of the program.')


if __name__ == '__main__':
    main()
