import logging
import sys

from modules.argparser import Argparser
from modules.connector import Connector
from modules.output import ConsoleOutput
from modules.rssparser import RSSparser
from modules.writer import WriterJSON

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

    if args['version']:
        print('\nVersion {}'.format(VERSION))
    else:
        if args['source'] is not None:

            if args['verbose']:  #
                logger.setLevel(logging.DEBUG)
                # logger.setLevel(logging.INFO)

            logger.info('Starting the program.')

            if Connector(url=args['source'], logger=logger).is_connected:
                news = RSSparser(url=args['source'], limit=args['limit'], logger=logger).parse_news()

                with ConsoleOutput(logger=logger) as console:
                    console.output(news)

                if args['json']:
                    WriterJSON(logger=logger, name='news').write(news)
            else:
                logger.debug('Closing the program.')

    logger.info('Termination of the program.')


if __name__ == '__main__':
    main()
