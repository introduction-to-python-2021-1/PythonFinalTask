import logging.handlers
import sqlite3
import sys

from reader import functions


def main(argv=sys.argv):
    args = functions.create_arguments(argv)
    """Creating logger"""
    logger = functions.create_logger()

    """Creating connection"""
    connection = sqlite3.connect('news.db')

    if args.get('limit'):
        limit = functions.check_limit(args.get('limit'))
    else:
        limit = 0

    if args.get('verbose'):
        """Turning on the output of messages about events"""
        logging.disable(0)
        logger.info('Checking for news to parse...')

    date = args.get('date')
    url = args.get('source')
    html = args.get('to_html')
    pdf = args.get('to_pdf')

    if not date:
        logger.info(
            f"Retrieves news from url ({url}) ...")
        result = functions.get_from_url(url)
        functions.store_news(result, connection, url)
    else:
        logger.info(
            f"Retrieves news for the selected date ({date}) ...")
        result = functions.get_from_db(date, url, connection)
        if html:
            functions.save_news_in_html_file(result, html, logger)
        if pdf:
            functions.pdf_factory(result, pdf, logger)

    if limit > 0:
        logger.info(f'Working with limited by user number ({limit} items) of articles')
        logger.info('Creating the list of news for limited articles...' + '\n')
        for item in result[:limit]:
            if args.get('json'):
                json_item = functions.make_json(item)
                print(json_item)
            else:
                print(item)
            if html:
                functions.save_news_in_html_file(result[:limit], html, logger)
            if pdf:
                functions.pdf_factory(result[:limit], pdf, logger)
        logger.info('The list of news was created successfully!')
    elif args.get('json'):
        logger.info('Creating the list of news in json format...')
        for item in result:
            json_item = functions.make_json(item)
            print(json_item)
        if html:
            functions.save_news_in_html_file(result, html, logger)
        if pdf:
            functions.pdf_factory(result, pdf, logger)
        logger.info('The list of news was created successfully!')
    else:
        logger.info('Creating the list of news...')
        for article in result:
            print(article)
        logger.info('The list of news was created successfully!')
        if html:
            functions.save_news_in_html_file(result, html, logger)
        if pdf:
            functions.pdf_factory(result, pdf, logger)


if __name__ == '__main__':
    main()
