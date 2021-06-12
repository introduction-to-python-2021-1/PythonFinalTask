import logging.handlers
import pathlib
import sqlite3
import sys

from reader import functions
from reader.colorize_logger import ColorizeLogger


def main(argv=sys.argv):
    args = functions.create_arguments(argv)
    # Creating logger
    logger = ColorizeLogger()

    if args.get('colorize'):
        logger.is_colorize = True

    # Creating connection
    db = str(pathlib.Path(__file__).parent.absolute()) + '\\news.db'
    connection = sqlite3.connect(db)

    functions.init_database(connection)

    if args.get('limit'):
        limit = functions.check_limit(args.get('limit'))
    else:
        limit = 0

    if args.get('verbose'):
        # Turning on the output of messages about events
        logging.disable(0)
        logger.info('Checking for news to parse...')

    date = args.get('date')
    url = args.get('source')
    html = args.get('to_html')
    pdf = args.get('to_pdf')

    logger.info(f"Downloading news from {url}...")
    result = functions.get_from_url(url)
    functions.store_news(result, connection, url)
    if date:
        result = functions.get_from_db(date, url, connection, logger)
        logger.info(f"Retrieves news for the selected date ({date}) from database...")

    if limit > 0:
        logger.info(f'Working with limited by user number ({limit} items) of articles...')
        logger.info('Creating the list of news...' + '\n')
        result = result[:limit]
    if args.get('json'):
        logger.info('Converting to json format...')
        for item in result:
            json_item = functions.make_json(item)
            logger.print(json_item)
    else:
        for article in result:
            logger.print(article)

    logger.info('The list of news was created successfully!')

    if pdf or (html and pdf):
        functions.save_news_in_pdf_file(result, pdf, logger, html)
    if html and pdf is None:
        functions.save_news_in_html_file(result, html, logger)


if __name__ == '__main__':
    main()
