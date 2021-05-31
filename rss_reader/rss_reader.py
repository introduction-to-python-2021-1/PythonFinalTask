"""
Module parses RSS feed https://news.yahoo.com/rss/
"""

import argparse
import json
import logging
import sys

from bs4 import BeautifulSoup
import requests


def print_news_to_shell(news_dict):
    """
    Function accepts dict with news items and prints it to shell.
    :param news_dict:
    :return: None
    """
    logging.info('Printing news items to shell.')
    # print meta data
    print(f"Feed: {news_dict['Feed']}")
    print(f"Items count: {news_dict['Items count']}")
    # Loop through news items and print out
    for i in news_dict['Items']:
        print()
        for key, value in i.items():
            print(f'{key}: {value}')


def dump_news_to_json(news_dict, file_path):
    """
    Function accepts dict with news items and saves it to json file.
    :param news_dict: type dict
    :return: None
    """
    with open(file_path, 'w') as f_object:
        json.dump(news_dict, f_object, indent=4, ensure_ascii=False)
    logging.info(f'Dumped {len(news_dict["Items"])} news items to json.')


def collect_news_items(soup_object, limit):
    """
    Function accepts bs4 object and limit, and extracts news items to dict.
    :param soup_object: type bs4.BeautifulSoup
    :param limit: type int
    :return: dict
    """
    news_to_dict = {'Feed': soup_object.channel.title.text, 'Items count': 0, 'Items': []}  # Initialize output dictionary
    use_limit = True if limit > 0 else False # - initialize use_limit flag; if False or 0 - collect all news items
    logging.info(f'Use limit: {use_limit}. Limit value: {limit}')
    # Loop through news items and add them to the dictionary, using args.limit
    logging.info('Looping through news items.')
    for i in soup_object.find_all('item'):
        item_dict = dict()  # initialize 1 news item dictionary and fill below
        item_dict['Title'] = i.title.text
        item_dict['Date'] = i.pubDate.text.replace('T', ' ').replace('Z', '')
        item_dict['Link'] = i.link.text
        item_dict['Source'] = i.source.text
        news_to_dict['Items'].append(item_dict)
        if use_limit:
            limit -= 1
            if limit == 0: break
    news_to_dict['Items count'] = len(news_to_dict["Items"])
    logging.info(f'News items collected to dict: {len(news_to_dict["Items"])} items in total.')
    return news_to_dict


def shut_down():
    """
    Function exits the program prematurely on error.
    :return: None
    """
    logging.info('Shutting down.')
    sys.exit(1)


def initialize_logging(verbose_on):
    """
    Function initializes logging on program start.
    If "--verbose" is on, the program prints logs to stdout.
    If "--verbose" is off, the program prints logs to log file "rss_reader.log".
    :param verbose_on: bool
    :return: None
    """
    log_filename = 'rss_reader.log'
    log_settings = dict(filename=log_filename, level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')
    if verbose_on: del log_settings['filename']
    logging.basicConfig(**log_settings)
    logging.info(f'STARTING PROGRAM. User passes arguments: {sys.argv}')


def check_URL_validity():
    """
    Function checks if user enters empty or invalid URL, checks connection status code.
    :return: True if URL and connection OK, False if invalid URL or bad response.
    """
    if len(sys.argv) > 1:
        if sys.argv[1] not in allowed_arguments:
            # Check connection
            r = requests.get(sys.argv[1])
            if r.status_code == 200:
                logging.info('Connection OK.')
                return True
            else:
                logging.info(f'Invalid URL. {add_log_msg}')
                print(f'Please, enter a valid URL of an RSS feed. "{sys.argv[1]}" seems to be wrong.')
                return False
        else:
            logging.info(f'URL not provided. {add_log_msg}')
            print('Please, provide a valid URL.')
            return False
    else:
        logging.info(f'Invalid arguments. {add_log_msg}')
        print(f'Please, enter valid arguments. Must include URL of RSS feed and optionals: {allowed_arguments}.')
        return False


def misspelled_args():
    """
    Function checks if user enters any misspelled arguments, excluding negative numbers.
    :return: True or False
    """
    if len(sys.argv) > 1:
        misspelled_args_list = list()
        list_to_check = [item for item in sys.argv[1:] if item.strip('-').isalpha()] # exclude numeric
        for item in list_to_check:
            if item.startswith('-') and item not in allowed_arguments:
                misspelled_args_list.append(item)
        if misspelled_args_list:
            logging.info(f'User misspelled some arguments: {misspelled_args_list}. {add_log_msg}')
            print(f"Looks like you've misspelled some arguments: {misspelled_args_list}")
            return True
    else:
        return False


def get_soup_object(args_source):
    """
    Function returns soup object from URL.
    :param args_source: string, link to RSS feed
    :return: soup object or None
    """
    r = requests.get(args_source)
    soup = BeautifulSoup(r.content, features='xml')
    if soup.rss:
        logging.info('Got soup.')
        return soup
    else:
        logging.info(f'The URL is not a valid RSS feed. {add_log_msg}')
        print('This URL is not a valid RSS feed.')
        shut_down()
        return None


def parsed_args():
    """
    Initializes argument parser, collects arguments from user. Returns user arguments
    if they are valid and connection is OK. Else returns None and shuts the program down with "shut_down()" function.
    :return: parser.parse_args(), type = argparse.Namespace
    """
    # Parser
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    # Positional arguments
    parser.add_argument('source', type=str, help='RSS URL')
    # Optional arguments
    parser.add_argument('--version', action='version', version='"Version 1.2"', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=0, help='Limit news topics if this parameter provided')
    # Sanity checks:
    # - misspelled arguments
    # - help, version
    # - URL validity
    # - limit
    if misspelled_args():
        shut_down()
    elif any(item in args_for_quick_exit for item in sys.argv): # quick exit - help or version
        parser.parse_args()
    elif check_URL_validity():
        user_args = parser.parse_args()
        # also check limit, must be >= 0
        if '--limit' in sys.argv:
            if user_args.limit < 0:
                logging.info(f'User entered negative limit. {add_log_msg}')
                print('Warning: Limit must be positive or 0. Enter a valid limit.')
                shut_down()
            else:
                return user_args
        else:
            return user_args
    else:
        shut_down()


def main():
    """
    Function runs the program.
    :return:
    """
    initialize_logging('--verbose' in sys.argv)
    args = parsed_args() # Run parser
    soup_object = get_soup_object(args.source) # Get soup object
    news_items = collect_news_items(soup_object, args.limit) # Collect news items into dictionary
    # Dump news items to file if user selects --json option
    if args.json: dump_news_to_json(news_items, rss_output_path)
    # Print out to shell
    if news_items: print_news_to_shell(news_items)
    logging.info('Program end.')


# python3 rss_reader.py https://news.yahoo.com/rss/ --limit 1 --json
args_for_quick_exit = ['--version', '-h', '--help']
allowed_arguments = ['-h', '--help', '--version', '--json', '--verbose', '--limit']
rss_output_path = 'news_from_rss.json'
add_log_msg = 'Printing message to shell.'

if __name__ == '__main__':
    main()