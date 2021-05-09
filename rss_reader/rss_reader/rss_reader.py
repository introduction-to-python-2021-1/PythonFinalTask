import argparse
import feedparser
import re
import logging
import json


import requests
from requests.exceptions import RequestException

__version__ = 1.1

LINK_TYPES = {
    'text/html': 'link',
    'image/jpeg': 'image',
    'image/png': 'image',
    'image/gif': 'gif',
    'video/mp4': 'video',
}

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def parse_cmd_args():
    """Returns arguments passed to the command line.

    :return: dictionary of arguments and their values passed to cmd (dict)
    """

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL', nargs='?')
    parser.add_argument('--version', help='Print version info', action='store_true')
    parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided', default=False)
    args = parser.parse_args()
    if args.source is None and args.version is False:
        print('''usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source
rss_reader.py: error: the following arguments are required: source''')
    return args.__dict__


def check_url_connection(url):
    """Detect an internet connection."""
    logger.debug('Checking the connection to the server...')
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        logger.debug('Connection detected.')

        rss = feedparser.parse(url)
        if len(rss['entries']) == 0:
            logger.error('Invalid URL. RSS feed not found.')
            conn = False
        else:
            conn = True

    except RequestException:
        logger.error('Connection not detected.')

        conn = False
    return conn


def parse_rss(url, limit=False):
    """Parses RSS feed, returns a description of each news

    :param url: link to RSS feed (str)
    :param limit: limiting the number of news (int)
    :return: list of dictionaries with information about each news (list)
    """

    rss = feedparser.parse(url)
    logger.debug('RSS feed received.')
    logger.debug('Parsing of the RSS feed started...')

    category_title = rss.feed.get('title')
    feeds = rss.get('entries')
    parsed_feeds = []

    if limit == 0 or limit < 0 or limit > len(feeds):
        limit = len(feeds)
    else:
        logger.debug('Limit on the number of news: {}.'.format(limit))

    for i in range(limit):
        feed_data = dict()
        feed_data['feed'] = category_title
        feed_data['title'] = feeds[i].get('title')
        feed_data['link'] = feeds[i].get('link')
        feed_data['date'] = feeds[i].get('published')

        feed_description = feeds[i].get('description')
        if feed_description is not None:
            rss_feed_description_parsed = clean_txt(feed_description)
            feed_data['description'] = rss_feed_description_parsed

        feed_links = feeds[i].get('links')
        if feed_links is not None:
            list_of_links = [{'link': link.get('href'), 'type': LINK_TYPES.get(link.get('type'))} for link in
                             feed_links]
            feed_data['links'] = list_of_links

        parsed_feeds.append(feed_data)

    logger.debug('Parsing of the RSS feed finished.')
    return parsed_feeds


def print_feed(feeds):
    """Print news to console

    :param feeds: list of news and their description (list)
    :return: None
    """
    logger.debug('News printing has started.')
    for feed in feeds:
        print('\nFeed: {}'.format(feed['feed']))
        print('\nTitle: {}'.format(feed['title']))
        print('Date: {}'.format(feed['date']))
        print('Link: {}\n'.format(feed['link']))

        if feed.get('description') is not None:
            print(feed['description'])
            print()

        if feed.get('links') is not None:
            links = feed.get('links')
            print('Links:')
            for i in range(len(links)):
                print('[{}] {} ({})'.format(i + 1, links[i].get('link'), links[i].get('type')))


def write_json(data, path='feeds.json'):
    """Writes the final news to the "feeds.json" file

    :param data: list of news and their description (list)
    :param path: Name or path to the file for recording (str)
    :return: None
    """
    logger.debug('Recording news in JSON file')
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=3)
            logger.debug('News recorded successfully.')
    except EnvironmentError:
        logger.error('Error writing to file')


def clean_txt(txt):
    """Clean txt from html tags

    :param txt: data containing html tags (str)
    :return: text without html tags (str)
    """
    cleaned = re.sub(r'<.*?>', '', txt)  # remove html
    cleaned = cleaned.replace('&lt;', '<').replace('&gt;', '>')
    cleaned = cleaned.replace('&quot;', '"')
    cleaned = cleaned.replace('&rsquo;', "'")
    cleaned = cleaned.replace('&nbsp;', ' ')
    return cleaned


def main():
    args = parse_cmd_args()  # Получаем аргументы, переданные в командную строку
    if args['source'] is not None:  # Проверяем, передан ли URL
        if args['verbose']:  # Проверяем, установлен ли флаг --verbose
            logger.setLevel(logging.DEBUG)
            # logger.setLevel(logging.INFO)

        logger.info('Starting the program.')
        if check_url_connection(args['source']):  # Проверяем соединение с переданным URL

            feeds = parse_rss(args['source'], args['limit'])  # Парсим RSS ленту
            print_feed(feeds)  # Выводим новости в консоль

            if args['json']:
                write_json(feeds)
        else:
            logger.debug('Closing the program.')

    if args['version']:
        print('\nVersion {}'.format(__version__))
    logger.info('Termination of the program.')


if __name__ == '__main__':
    main()
