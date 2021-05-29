"""
Main module of rss_reader
"""


import os
from rss_reader.argparser import get_args
from rss_reader.logger_conf import create_root_logger, add_console_handler
from rss_reader.RssParser import RssParser
from rss_reader.cache_handlers import get_feed_from_cache, print_cached_feed
from rss_reader.pdf_converter import convert_to_pdf
from rss_reader.html_converter import convert_to_html


def main():
    arguments = get_args()

    logger = create_root_logger()

    if arguments.verbose:
        add_console_handler(logger)

    logger.info('Starting script')

    if not arguments.url:
        raise ValueError("URL is empty, please input URL")

    logger.info(f'Program started, url: {arguments.url}')

    if arguments.date:
        feed_list = get_feed_from_cache(arguments.date, arguments.limit)
        print(print_cached_feed(feed_list))
    else:
        get_data = RssParser(arguments.url, arguments.limit)
        try:
            get_data.get_feed()

        except Exception as error_message:
            logger.error(error_message)
            if not arguments.verbose:
                print(error_message)

        if arguments.json:
            print(get_data.convert_to_json())

        elif not arguments.to_pdf and not arguments.to_html:
            print(get_data)

        if arguments.to_pdf:
            path_to_pdf_file = arguments.to_pdf + os.path.sep + 'news.pdf'
            try:
                convert_to_pdf(get_data, path_to_pdf_file)
            except Exception as err:
                logger.error(err)
                if not arguments.verbose:
                    print(err)

        if arguments.to_html:
            path_to_html_file = arguments.to_html + os.path.sep + 'news.html'
            try:
                convert_to_html(get_data, path_to_html_file)
            except Exception as err:
                logger.error(err)
                if not arguments.verbose:
                    print(err)


if __name__ == '__main__':
    main()
