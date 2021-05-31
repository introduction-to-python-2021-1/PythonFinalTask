"""
This module provides tools for working with cache
"""

import os
import json
import time
from collections import namedtuple


def get_feed_from_cache(date, limit):
    """
    Open cache file and takes specified number of news with the corresponding date
    :param date: News date
    :param limit: Number of news to be added
    :return: List with news items
    """
    dir_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + 'feed_cache' + os.path.sep + date + '.json'
    try:
        with open(dir_path) as dp:
            news = json.load(dp)
            return news[:limit]
    except FileNotFoundError:
        print('Can\'t find news with this date')
    return False


def save_feed_into_cache(item):
    """
    This function saves feed item into file in json format
    :param item: feed item
    """
    date = time.strftime('%Y%m%d', item.date)
    dir_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + 'feed_cache' + os.path.sep
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path = dir_path + date + '.json'
    item_to_cache = json.dumps(item._asdict(), ensure_ascii=False)
    with open(file_path, 'a', encoding='utf-8') as fp:
        if os.stat(file_path).st_size == 0:
            feed_list = [item_to_cache]
            json.dump(feed_list, fp)
            return
    with open(file_path, encoding='utf-8') as fp:
        feed_list = json.load(fp)
        if item_to_cache in feed_list:
            return
        feed_list.append(item_to_cache)
    with open(file_path, 'w', encoding='utf-8') as fp:
        json.dump(feed_list, fp)
    return


def create_item_list_from_cache(list_with_feed):
    """
    Creates list with feed items from cached feed
    :param list_with_feed: list with cached feed
    :return: list with feed items
    """
    data = []
    for item in list_with_feed:
        loaded_dict = json.loads(item)
        tuple_item = namedtuple('item', loaded_dict)
        item = tuple_item(**loaded_dict)
        data.append(item)
    return data
