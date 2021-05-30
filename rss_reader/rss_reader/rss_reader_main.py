"""
Main module of rss_reader
"""
import json
import os
import sys

from rss_reader.argparser import get_args
from rss_reader.logger_conf import create_root_logger, add_console_handler
from rss_reader.RssParser import RssParser, convert_to_json
from rss_reader.cache_handlers import get_feed_from_cache, print_cached_feed
from rss_reader.pdf_converter import convert_to_pdf
from rss_reader.html_converter import convert_to_html
from collections import namedtuple


def main():
    arguments = get_args()

    logger = create_root_logger()

    if arguments.verbose:
        add_console_handler(logger)

    logger.info('Starting script')
    logger.info(f'Program started, url: {arguments.url}')

    if arguments.date:
        if arguments.url:
            get_data = RssParser(arguments.url, arguments.limit)
            if not get_data:
                sys.exit()

            get_data.get_feed()

        feed_list = get_feed_from_cache(arguments.date, arguments.limit)
        if not arguments.to_pdf and not arguments.to_html and not arguments.json:
            print(print_cached_feed(feed_list))
        else:
            data = []
            for item in feed_list:
                if arguments.json:
                    logger.info('Printing feed in json format')
                    print(item)
                loaded_dict = json.loads(item)
                tuple_item = namedtuple('item', loaded_dict)
                item = tuple_item(**loaded_dict)
                data.append(item)

            if arguments.to_pdf:
                logger.info('Converting feed to pdf')
                path_to_pdf_file = arguments.to_pdf + os.path.sep + 'news.pdf'
                convert_to_pdf(data, path_to_pdf_file)

            if arguments.to_html:
                logger.info('Converting feed to html')
                path_to_html_file = arguments.to_html + os.path.sep + 'news.html'
                convert_to_html(data, path_to_html_file)

    else:
        get_data = RssParser(arguments.url, arguments.limit)
        if not get_data:
            sys.exit()

        data = get_data.get_feed()

        if not arguments.to_pdf and not arguments.to_html and not arguments.json:
            print(get_data)

        if arguments.json:
            logger.info('Printing feed in json format')
            print(convert_to_json(data))

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
