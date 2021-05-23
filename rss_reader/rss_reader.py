import feedparser
import collections
import time
import json
import requests
from bs4 import BeautifulSoup
import argparse
import logging
import os


def create_root_logger():
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler('reader.log')
    file_handler.setFormatter(formatter)
    root_logger = logging.getLogger('logger')
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    return root_logger


def add_console_handler(logger_to_update):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger_to_update.addHandler(console_handler)
    return logger_to_update


def get_img(link):
    img_list = []
    request = requests.get(link)
    soup = BeautifulSoup(request.text, 'lxml')
    img_container = soup.find_all('div', class_='caas-img-container')
    for container in img_container:
        if container:
            for img in container.find_all('img'):
                clean_text = BeautifulSoup(img.get('alt'), "lxml").text
                if img.get('src'):
                    img_dict = {'src': img.get('src'), 'alt': clean_text}
                    img_list.append(img_dict)
    return img_list


def get_args():
    parser = argparse.ArgumentParser(description='Python RSS-reader',
                                     prog='rss_parser',
                                     )

    parser.add_argument('url',
                        type=str,
                        help='URL to parse.',
                        )

    parser.add_argument('--limit',
                        type=int,
                        default=None,
                        help='Limit news topics if provided',
                        )

    parser.add_argument('--verbose',
                        action='store_true',
                        help='Outputs verbose status messages',
                        )

    parser.add_argument('--json',
                        action='store_true',
                        help='Outputs news in json format',
                        )

    parser.add_argument('--version',
                        action='version',
                        version='Rss reader 1.0.',
                        help='Prints version and stop',
                        )

    parser.add_argument('--date',
                        type = str,
                        help = 'Return news with the specified data',
                        default = '',
                        )

    args = parser.parse_args()
    return args


def get_feed_from_cache(date, limit):
    file_path = os.path.abspath(os.path.dirname('app'))
    file_path += os.path.sep + 'feed_cache' + os.path.sep + date + '.json'
    try:
        with open(file_path) as fp:
            news = json.load(fp)
            return news[:limit]
    except FileNotFoundError:
        print('Can\'t find news with this date')
    return False


def print_cached_feed(feed_list):
    for feed in feed_list:
        loaded_feed = json.loads(feed)
        print(loaded_feed.keys())
        print(loaded_feed['title'])
        print(loaded_feed['link'])
        print(time.strftime("%y-%m-%d %H:%M", tuple(loaded_feed['date'])))
        if loaded_feed['img']:
            print(loaded_feed['img'])
        if loaded_feed['content']:
            print(loaded_feed['content'])


class RssParser:
    def __init__(self, url, limit):
        self.url = url
        self.limit = limit
        self.items = []
        self.name = ''

    def get_feed(self):
        data = feedparser.parse(self.url)
        if data['bozo']:
            raise ValueError("Please check URL and Internet connection")
        self.name = data['feed'].get('title')
        self.get_content(data)
        return self.items

    def get_content(self, data):
        for feed in data['entries'][:self.limit]:
            title = feed.get('title', 'Absence of title')
            link = feed.get('link', 'Absence of link')
            date = feed.get('published_parsed')
            img = get_img(link)
            summary_list = []
            if feed.get('summary'):
                summary_list.append(feed.get('summary'))
            item = collections.namedtuple('item', 'title, link, date, img, content')._make((title, link, date, img, summary_list))
            self.save_feed_into_cache(item)
            self.items.append(item)

    def convert_to_json(self, item):
        return json.dumps({'url': self.url,
                           'feed': {'name': self.name,
                                    'items': [item._asdict() for item in self.items]}}, ensure_ascii=False)

    def save_feed_into_cache(self, item):
        date = time.strftime('%Y%m%d', item.date)
        dir_path = os.path.abspath(os.path.dirname('app')) + os.path.sep + 'feed_cache' + os.path.sep
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_path = dir_path + date + '.json'
        item_to_cache = json.dumps(item._asdict(), ensure_ascii=False)
        print('trying to open')
        with open(file_path, 'a', encoding='utf-8') as fp:
            if os.stat(file_path).st_size == 0:
                feed_list = [item_to_cache]
                json.dump(feed_list, fp)
                return
        with open(file_path, 'r', encoding='utf-8') as fp:
            feed_list = json.load(fp)
            if item_to_cache in feed_list:
                return
            feed_list.append(item_to_cache)
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(feed_list, fp)
        return


    def __str__(self):
        result_str = self.name + '\n'
        for item in self.items:
            item_as_str = f'Title: {item.title}\nLink: {item.link}\nDate: {time.strftime("%y-%m-%d %H:%M", item.date)}\n'
            result_str += item_as_str
            if item.content:
                result_str += 'Content: '
                for stuff in item.content:
                    result_str += stuff + '\n'
            for num, img in enumerate(item.img):
                images_as_str = f'Image № {str(num + 1)}: {img["src"]}'
                result_str += images_as_str + '\n'
                if img['alt']:
                    img_desc = f'Description: {img["alt"]}'
                    result_str += img_desc + '\n'
            result_str += '\n\n'
        return result_str


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
        print_cached_feed(feed_list)
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
        else:
            print(get_data)
        logger.info(f'Program finished, {len(get_data.items)} news was showed')

if __name__ == '__main__':
    main()
