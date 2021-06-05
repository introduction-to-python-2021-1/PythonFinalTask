"""
Main module of rss_reader
"""


import os
import sys
from rss_reader.argparser import get_args
from rss_reader import logger_conf
from rss_reader import rss_parser
from rss_reader import cache_handlers
from rss_reader.pdf_converter import convert_to_pdf
from rss_reader.html_converter import convert_to_html


def main():
    arguments = get_args()
    logger = logger_conf.create_root_logger()
    if arguments.verbose:
        logger_conf.add_console_handler(logger)
    logger.info('Starting script')
    if arguments.limit is not None and arguments.limit <= 0:
        print('limit should be positive number')
        sys.exit()
    logger.info(f'Program started, url: {arguments.url}')
    if arguments.date:
        if arguments.url:
            parsed_data = rss_parser.RssParser(arguments.url, arguments.limit)
            parsed_data.get_feed()
        feed_list = cache_handlers.get_feed_from_cache(arguments.date, arguments.limit)
        data = cache_handlers.create_item_list_from_cache(feed_list)
    else:
        parsed_data = rss_parser.RssParser(arguments.url, arguments.limit)
        feed = parsed_data.get_feed()
        data = feed[:arguments.limit]
    if not arguments.to_pdf and not arguments.to_html and not arguments.json:
        print(rss_parser.print_feed(data))
    if arguments.json:
        logger.info('Printing feed in json format')
        print(rss_parser.convert_to_json(data))
    if arguments.to_pdf:
        logger.info('Converting feed to pdf')
        path_to_pdf_file = arguments.to_pdf + os.path.sep + 'news.pdf'
        convert_to_pdf(data, path_to_pdf_file)
    if arguments.to_html:
        logger.info('Converting feed to html')
        path_to_html_file = arguments.to_html + os.path.sep + 'news.html'
        convert_to_html(data, path_to_html_file)


if __name__ == '__main__':
    main()
