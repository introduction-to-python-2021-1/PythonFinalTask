from argparser import get_args
from rss_reader import RssParser
import logger_conf


def main():
    arguments = get_args()

    logger = logger_conf.root_logger

    if arguments.verbose:
        logger_conf.add_console_handler(logger)

    logger.info('Starting script')

    if not arguments.url:
        raise ValueError("URL is empty, please input URL")

    logger.info(f'Program started, url: {arguments.url}')
    get_data = RssParser(arguments.url, arguments.limit)
    try:
        get_data.get_feed()
    except Exception as error_message:
        logger.error(error_message)
        if not arguments.verbose:
            print(error_message)

    if arguments.json:
        print(get_data.convert_to_json())
    else:
        print(get_data)
    logger.info('Program finished')


if __name__ == '__main__':
    main()
