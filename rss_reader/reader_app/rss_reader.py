"""
Program parses RSS feed https://news.yahoo.com/rss/
"""
import argparse
import datetime
import json
import logging
import os
import pprint
import sys
import urllib.request

from bs4 import BeautifulSoup
from PIL import Image
import requests
from reader_app import rss_conversion
import validators
import urllib.request
from urllib.error import URLError


def logging_settings(verbose_mode):
    """
    Function sets logging level to INFO or CRITICAL depending on '--verbose' option.
    :param verbose_mode: (bool) if '--verbose' in sys.argv
    :return: (dict) logging_settings_dict
    """
    if verbose_mode:
        logging_level = 20
    else:
        logging_level = 999
    logging_settings_dict = dict(level=logging_level, format='%(asctime)s [%(levelname)s] %(message)s')
    return logging_settings_dict


def run_parser(user_args):
    """
    Initializes argument parser.
    :param user_args: sys.argv[1:]
    :return: parsed arguments (argparse.Namespace)
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    # Positional argument
    parser.add_argument('source', type=str, help='RSS URL')
    # Optional arguments
    parser.add_argument('--version', action='version', version=f'"Version {VERSION}"', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=0, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=int, help='Publishing date')
    parser.add_argument('--to-pdf', type=str, default='', help='Converts output to PDF format. Enter path')
    parser.add_argument('--to-html', type=str, default='', help='Converts output to HTML format. Enter path')
    return parser.parse_args(user_args)


def force_close(error_msg):
    """
    Forcefully shuts the program down after error.
    :return: None
    """
    logging.error('Shutting down.')
    quit(error_msg)


def get_soup_object(r_content):
    """
    Returns bs4 object from request content.
    :param r_content: (request content)
    :return: soup (bs4.BeautifulSoup)
    """
    soup = BeautifulSoup(r_content, features='xml')
    try:
        if 'Yahoo News - Latest News' in soup.rss.channel.title.text:
            logging.info('Retrieved bs4 object from requested URL.')
            return soup
    except AttributeError:
        logging.error('Provided URL is not Yahoo News RSS feed.')
        force_close('Please, provide Yahoo News RSS feed URL.')


def collect_news_items(soup_obj, real_cwd):
    """
    Function extracts news items from bs4 object and puts them in dict.
    Also saves images to news items to 'local_storage/images'
    :param soup_obj: (bs4)
    :param real_cwd: (str) real current working directory
    :return:
    """
    # images new width
    new_width = 300
    # get image directory path
    img_dir_path = os.path.join(real_cwd, 'local_storage', 'images')

    news_to_dict = {'Feed': soup_obj.channel.title.text, 'Items count': 0, 'Items': []}  # Initialize output dictionary
    # Loop through news items and add them to the dictionary, using limit
    logging.info('Looping through news items. Collecting them into dictionary. '
                 'Resizing and saving images to local folder if available in news items. '
                 'This may take a while...')
    for img_id, item in enumerate(soup_obj.find_all('item')):
        item_dict = dict()  # initialize 1 news item dictionary and fill below
        item_dict['Title'] = item.title.text
        date_and_time = (item.pubDate.text.replace('T', ' ').replace('Z', '')).split(' ')
        item_dict['Date'] = date_and_time[0]
        item_dict['Time'] = date_and_time[1]
        item_dict['Link'] = item.link.text
        item_dict['Source'] = item.source.text
        # get image URL
        if item.content:
            image_save_path = os.path.join(img_dir_path, f'{img_id:02d}.png')
            item_dict['Image'] = {'URL': item.content['url'], 'Path': image_save_path}
            # Retrieve, resize, and save image to local folder
            im = Image.open(requests.get(item_dict['Image']['URL'], stream=True).raw)
            new_height = int(im.height / (im.width / new_width))
            im = im.resize((new_width, new_height))
            im.save(item_dict['Image']['Path'], optimize=True)
        else:
            # If image is unavailable, leave None
            item_dict['Image'] = {'URL': None, 'Path': None}
        news_to_dict['Items'].append(item_dict)
    news_to_dict['Items count'] = len(news_to_dict["Items"])
    return news_to_dict


def get_user_limit(news_items, requested_limit):
    """
    Function determines what news items limit will be used with json, date, conversion.
    :param news_items: (dict) dictionary of all news items to be cached later
    :param requested_limit: (int) user's input in '--limit'
    :return: (int)
    """
    if news_items['Items count'] > requested_limit > 0:
        result = requested_limit
    else:
        result = news_items['Items count']
    logging.info(f'Using news items limit {result}.')
    return result


def limit_news_items(news_complete, user_limit, filter_by_date=False, user_date=0):
    """
    Function takes complete news items dictionary and returns a copy containing news limited by date and --limit.
    :param news_complete: (dict) all news items
    :param user_limit: (int)
    :param filter_by_date: (bool)
    :param user_date: (int)
    :return: (dict)
    """
    if filter_by_date:
        try:
            user_date = get_date_obj(user_date)
        except ValueError:
            logging.error("Couldn't get date object from user input.")
            force_close('Unable to parse date from the specified value. Please, check your date input.')
            # return None

        result_news_items = list()
        # Loop through news items and include only by date and up to the limit.
        for news_item in news_complete['Items']:
            item_date_obj = datetime.datetime.strptime(news_item['Date'], "%Y-%m-%d").date()
            if item_date_obj == user_date:
                result_news_items.append(news_item)
                user_limit -= 1
                if user_limit == 0:
                    break
        result_dict = {'Feed': news_complete['Feed'], 'Items count': len(result_news_items), 'Items': result_news_items}
        return result_dict
    else:
        if news_complete['Items count'] > user_limit > 0:
            result_news_items = news_complete['Items'][:]
            del result_news_items[user_limit:]
            result_dict = {'Feed': news_complete['Feed'], 'Items count': len(result_news_items),
                           'Items': result_news_items}
            return result_dict
        else:
            return news_complete


def print_news_in_terminal(dict_to_print, json_mode):
    """
    Prints limited news items to shell.
    :return: None
    """
    logging.info(f'Printing news to shell. JSON mode is {json_mode}.')
    if json_mode:
        print('Printing news in JSON mode.')
        pp = pprint.PrettyPrinter()
        pp.pprint(dict_to_print)
    else:
        print('Printing news in text mode.')
        print(f"Feed: {dict_to_print['Feed']}")
        print(f"Items count: {dict_to_print['Items count']}")
        # Loop through news items and print out
        for i in dict_to_print['Items']:
            print()
            for key, value in i.items():
                if key == 'Image':
                    print(f'{key}:')
                    for key1, val1 in value.items():
                        print(f'\t{key1}: {val1}')
                else:
                    print(f'{key}: {value}')


def get_conversion_paths(user_args):
    """
    Function returns tuple: pdf_path, html_path
    :param user_args: args from sys.argv
    :return: (tuple)
    """
    if '--to-pdf' in user_args:
        pdf_path = user_args[user_args.index("--to-pdf") + 1]
    else:
        pdf_path = ''
    if '--to-html' in user_args:
        html_path = user_args[user_args.index("--to-html") + 1]
    else:
        html_path = ''
    return pdf_path, html_path


def get_date_obj(user_date):
    """
    Gets date object from user --date input.
    :param user_date: (int)
    :return: (datetime.date)
    """
    try:
        date_obj = datetime.datetime.strptime(str(user_date), '%Y%m%d').date()
        logging.info(f'Successfully parsed date.')
        return date_obj
    except ValueError:
        raise


def source_is_valid(user_url):
    """
    Checks if a URL is a valid source.
    :param user_url: (str)
    :return: (bool)
    """
    if validators.url(user_url):
        logging.info('Source is valid.')
        return True
    else:
        logging.error('Source is invalid.')
        return False


def connection_ok(host):
    """
    Function checks if internet connection is on.
    :param host: (str)
    :return: (bool)
    """
    try:
        urllib.request.urlopen(host)
        return True
    except URLError as e:
        logging.error(f'No internet connection. Details: {e}')
        return False


def main():
    """
    Runs the program.
    :return: None
    """
    # determine real working directory
    # depends on how the program is launched
    # if from "reader_app", then real work dir is one level up
    # otherwise it's os.getcwd()
    if os.path.basename(os.getcwd()) == 'reader_app':
        real_work_dir = os.path.dirname(os.getcwd())
    else:
        real_work_dir = os.getcwd()

    # determine path to local rss cache (json file)
    path_cache = os.path.join(real_work_dir, 'local_storage', 'rss_cache.json')

    # initialize logging
    logging.basicConfig(**logging_settings('--verbose' in sys.argv))
    logging.info('Starting program.')

    # Quick stop & exit. Check 1/2. Quick exit args or no arguments at all.
    if len(sys.argv) > 1 and any(item in sys.argv for item in ['-h', '--help', '--version']):
        run_parser(sys.argv)
    elif len(sys.argv) == 1:
        logging.error('No arguments provided.')
        force_close('Please, provide your arguments.')

    # Quick stop & exit. Check 2/2. No date, no valid source.
    src_ok = source_is_valid(sys.argv[1])
    if '--date' not in sys.argv and not src_ok:
        logging.error('No working arguments provided.')
        force_close('Please, provide arguments to work with: at least source or date. Type "-h / --help" for help.')

    # Decide between 2 cycles: small or full.
    # FETCH FROM LOCAL IF:
    # - has date
    # - source valid
    # - no connection
    # OR IF:
    # - has date
    # - no valid source
    if (
            ('--date' in sys.argv and src_ok and not connection_ok(sys.argv[1]))
            or
            ('--date' in sys.argv and not src_ok)
    ):
        # DO SMALL CYCLE
        logging.info('Doing SMALL cycle: Fetching news from local cache.')
        input_date = int(sys.argv[sys.argv.index("--date") + 1])
        with open(path_cache, 'r') as f_obj:
            news_from_local = json.load(f_obj)
        if news_from_local['Items count'] == 0:
            logging.error('Local storage empty')
            force_close('Sorry, no news items in local storage.')

        # determine user limit
        if '--limit' in sys.argv:
            user_limit = int(sys.argv[sys.argv.index("--limit") + 1])
            if user_limit < 0:
                logging.error('User enters negative or zero limit.')
                force_close('Please, enter a positive limit.')
        else:
            user_limit = 0

        # get conversion paths from user's arguments
        pdf_path, html_path = get_conversion_paths(sys.argv)

        # limit news by date and number
        limited_news_to_print = limit_news_items(news_from_local, user_limit, filter_by_date=True, user_date=input_date)
    else:
        # DO FULL CYCLE
        logging.info('Doing FULL cycle: download news to cache, limit with "--limit" and "--date" and print out.')

        # check internet connection
        if connection_ok(sys.argv[1]):
            logging.info('Connection is OK.')
        else:
            force_close('Unable to connect to URL. Please, check your internet connection or URL.')

        # PARSE ARGUMENTS WITH argparse
        args = run_parser(sys.argv[1:])

        # get pdf & html paths
        pdf_path, html_path = args.to_pdf, args.to_html

        # ensure the limit is positive
        if args.limit < 0:
            logging.error('User enters negative or zero limit.')
            force_close('Please, enter a positive limit.')

        # get soup object
        request_content = requests.get(args.source).content
        bs4_obj = get_soup_object(request_content)

        # collect news items
        all_news_dict = collect_news_items(bs4_obj, real_work_dir)

        # determine user_limit
        user_limit = get_user_limit(all_news_dict, args.limit)

        # dump all news to local cache
        with open(path_cache, 'w') as f_object:
            json.dump(all_news_dict, f_object, indent=4, ensure_ascii=False)
        logging.info('Dumped news items to local cache.')

        # get arguments to be used below in 'limit_news_items' function
        args_to_limit_news = {'news_complete': all_news_dict, 'user_limit': user_limit}

        # print news for specific date
        if args.date:  # add to kwargs for 'limit_news_items' function
            args_to_limit_news['filter_by_date'] = True
            args_to_limit_news['user_date'] = args.date

        # SAVE LIMITED NEWS ITEMS to print in stdout: as text or as json
        limited_news_to_print = limit_news_items(**args_to_limit_news)

    # print limited news items to stdout: as json or as text
    if limited_news_to_print['Items count'] == 0:
        logging.error('No news items for specified quantity and date.')
        force_close('Sorry, unable to find news items for specified date and limit.')
    else:
        print_news_in_terminal(limited_news_to_print, '--json' in sys.argv)
        # print in PDF if path provided
        if pdf_path:
            logging.info(f'Printing to pdf file at {pdf_path}.')
            rss_conversion.print_to_pdf(limited_news_to_print, real_work_dir, pdf_path)
        if html_path:
            logging.info(f'Printing to HTML file at {html_path}.')
            rss_conversion.print_to_html(limited_news_to_print, real_work_dir, html_path)

    logging.info('Closing program.')


VERSION = '1.68'
if __name__ == '__main__':
    main()
