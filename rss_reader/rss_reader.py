import feedparser
import collections
import time
import json
import requests
from bs4 import BeautifulSoup
import argparse
import logging


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

    args = parser.parse_args()
    return args


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
            date = time.strftime('%y-%m-%d %H:%M', feed.get('published_parsed'))
            img = get_img(link)
            summary_list = []
            if feed.get('summary'):
                summary_list.append(feed.get('summary'))
            item = collections.namedtuple('item', 'title, link, date, img, content')._make((title, link, date, img, summary_list))
            self.items.append(item)

    def convert_to_json(self):
        return json.dumps({'url': self.url,
                           'feed': {'name': self.name,
                                    'items': [item._asdict() for item in self.items]}}, ensure_ascii=False)

    def __str__(self):
        result_str = self.name + '\n'
        for item in self.items:
            item_as_str = f'Title: {item.title}\nLink: {item.link}\nDate: {item.date}\n'
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
    logger.info('Program finished')


if __name__ == '__main__':
    main()
