"""
Program parses RSS feed https://news.yahoo.com/rss/
"""
import argparse
import copy
import json
import logging
import os
import pprint
import sys

from bs4 import BeautifulSoup
import requests


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
    parser.add_argument('--to-epub', type=str, default='', help='Converts output to EPUB format. Enter path')
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
    logging.info('Retrieved bs4 object from requested URL.')
    return soup


def collect_news_items(soup_obj):
    """
    Function extracts news items from bs4 object and puts them in dict.
    :param soup_obj:
    :return:
    """
    news_to_dict = {'Feed': soup_obj.channel.title.text, 'Items count': 0, 'Items': []}  # Initialize output dictionary
    # Loop through news items and add them to the dictionary, using limit
    for i in soup_obj.find_all('item'):
        item_dict = dict()  # initialize 1 news item dictionary and fill below
        item_dict['Title'] = i.title.text
        date_and_time = (i.pubDate.text.replace('T', ' ').replace('Z', '')).split(' ')
        item_dict['Date'] = date_and_time[0]
        item_dict['Time'] = date_and_time[1]
        item_dict['Link'] = i.link.text
        item_dict['Source'] = i.source.text
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


def limit_news_items(news_complete, limit):
    """
    Function takes complete news items dictionary and deletes any items above the user limit.
    :param news_complete: (dict)
    :param limit: (int)
    :return: limited_dict or news_complete (dict)
    """
    if news_complete['Items count'] > limit > 0:
        limited_dict = copy.deepcopy(news_complete)
        del limited_dict['Items'][limit:]
        limited_dict['Items count'] = limit
        return limited_dict
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
                print(f'{key}: {value}')


def get_cache_path(current_work_dir):
    """
    Function checks current working directory to determine the path to local cache.
    If the program is launched as python3 rss_reader.py etc., then cwd is rss_reader.
    If setup.py is used, cwd is PythonFinalTask.
    :param current_work_dir: (str)
    :return: path (str)
    """
    storage_dir = 'local_storage'
    app_dir = os.path.dirname(current_work_dir)
    if os.path.basename(app_dir) != 'rss_reader':
        app_dir = os.path.join(app_dir, 'rss_reader')
    path = os.path.join(app_dir, storage_dir, 'rss_cache.json')
    return path


def main():
    """
    Runs the program.
    :return: None
    """
    path_cache = get_cache_path(os.getcwd())

    # initialize logging
    logging.basicConfig(**logging_settings('--verbose' in sys.argv))
    logging.info('Starting program.')

    # no source, has date, read from cache

    # has source, dump to cache
    args = run_parser(sys.argv[1:])

    # ensure the limit is positive
    if args.limit < 0:
        force_close('Please, enter a positive limit.')

    # source is valid - TBD

    # get soup object
    request_content = requests.get(args.source).content
    bs4_obj = get_soup_object(request_content)

    # collect news items
    all_news_dict = collect_news_items(bs4_obj)

    # determine user_limit
    user_limit = get_user_limit(all_news_dict, args.limit)

    # dump all news to local cache
    with open(path_cache, 'w') as f_object:
        json.dump(all_news_dict, f_object, indent=4, ensure_ascii=False)
    logging.info('Dumped news items to local cache.')

    # save limited news items to print in stdout: as text or as json
    limited_news = limit_news_items(all_news_dict, user_limit)

    # print limited news items to stdout: as json or as test
    print_news_in_terminal(limited_news, args.json)

    logging.info('Closing program.')


VERSION = '1.6'
if __name__ == '__main__':
    exit(main())
