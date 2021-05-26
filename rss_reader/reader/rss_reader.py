import sys
import logging.handlers
import sqlite3

import datetime

from reader.functions import make_json, check_limit, execute_news, create_arguments, check_URL


def main():
    """Creating logger"""
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler('../../../logs.txt')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.disable()

    """Creating connection to DB and cursor object"""
    connection = sqlite3.connect('news.db')
    cursor = connection.cursor()

    args = create_arguments()

    if args.limit:
        limit = check_limit(args.limit)
    else:
        limit = 0

    if args.verbose:
        """Turning on the output of messages about events"""
        logging.disable(0)
        logger.info('Parcing news...')

    if not args.date:
        result = check_URL(args.source, cursor, connection)
    else:
        try:
            args_date = (datetime.datetime.strptime(args.date, '%Y%m%d')).date()
            logger.info(
                f"Retrieves news for the selected date ({args_date}) ...")
            result = execute_news(args.date, cursor, args.source)
            if len(result) == 0:
                raise SystemExit(f"Sorry, there are no articles for {args_date}!")
        except ValueError:
            raise SystemExit('Please, enter the date in the following format: "YYYYMMDD".')

    if limit > 0:
        logger.info(f'Working with limited by user number ({limit} items) of articles')
        logger.info('Creating the list of news for limited articles...')
        for item in result[0:limit]:
            if args.json:
                json_item = make_json(item)
                print(json_item)
            else:
                print(item)
        logger.info('The list of news was created successfully!')
    elif args.json:
        logger.info('Creating the list of news in json format...')
        for item in result:
            json_item = make_json(item)
            print(json_item)
        logger.info('The list of news was created successfully!')
    else:
        logger.info('Creating the list of news...')
        for article in result:
            print(article)
        logger.info('The list of news was created successfully!')


if __name__ == '__main__':
    main()
