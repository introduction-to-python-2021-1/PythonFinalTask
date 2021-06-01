"""
This module contains class for fetching and showing rss-feed
"""
import sys

import feedparser
from collections import namedtuple
import time
import json
from rss_reader.cache_handlers import save_feed_into_cache
from rss_reader import string_handlers
from rss_reader.image_handlers import get_img_container, if_link_is_image


class RssParser:
    """
    This class parses rss-feed and presents it in readable format
    """
    def __init__(self, url, limit):
        self.url = url
        self.limit = limit
        self.items = []
        self.name = ''

    def get_feed(self):
        """
        This function parses rss-feed
        :return: list with namedtuples representing feed items
        """
        if not self.url:
            print('URL is empty, please input URL')
            sys.exit()
        data = feedparser.parse(self.url)
        if data['bozo']:
            print('Please check URL(is RSS?) and Internet connection')
            sys.exit()
        self.get_content(data)
        return self.items

    def get_content(self, data):
        """
        This function aggregates feed from row data
        :param data: a bunch of row data
        """
        self.name = name = data['feed'].get('title')
        for feed in data['entries'][:self.limit]:
            title = feed.get('title', 'Absence of title')
            link = feed.get('link', 'Absence of link')
            date = feed.get('published_parsed', 'Absence of date')
            img = get_img_container(link)
            summary_list = []
            links = []
            if feed.get('summary'):
                summary_list = [feed.get('summary')]
            if feed.get('links'):
                uncleaned_links = feed.get('links')
                links = string_handlers.get_links(uncleaned_links)
                img.extend(if_link_is_image(uncleaned_links))
            fields = 'name, title, link, date, img, content, links'
            item = namedtuple('item', fields)._make((name, title, link, date, img, summary_list, links))
            save_feed_into_cache(item)
            self.items.append(item)


def print_feed(list_with_items):
    """
    Prints feed in readable format
    """
    result_str = list_with_items[0].name
    for item in list_with_items:
        item_as_str = (f'Title: {item.title}\nLink: {item.link}\n'
                       f'Date: {time.strftime("%y-%m-%d %H:%M", tuple(item.date))}')
        result_str += item_as_str
        result_str += string_handlers.get_str_content(item.content)
        result_str += string_handlers.get_img_as_str(item.img)
        result_str += string_handlers.get_links_as_str(item.links) + '\n\n'
    return result_str


def convert_to_json(data):
    """
    Converts feed items in json format
    """
    return json.dumps({'items': [item._asdict() for item in data]}, ensure_ascii=False)


def print_json(json_data):
    """
    Prints out feed converted to json in readable format
    """
    loaded_json_data = json.loads(json_data)
    print('Items: ')
    for item in loaded_json_data['items']:
        print(item)
        print('\n')
