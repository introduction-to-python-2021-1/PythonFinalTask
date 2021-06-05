"""
This module provides tools for working with cache
"""

import os
import json
import sys
from collections import namedtuple
from dateutil.parser import parse
import time


def get_feed_from_cache(date, limit):
    """
    Open cache file and takes specified number of news with the corresponding date
    :param date: News date
    :param limit: Number of news to be added
    :return: List with news items
    """
    check_if_date_correct(date)
    dir_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + 'feed_cache' + os.path.sep + date + '.json'
    try:
        with open(dir_path) as dp:
            news = json.load(dp)
            return news[:limit]
    except FileNotFoundError:
        print('Can\'t find news with this date, make sure you entered date in correct format yyyymmdd')
        return sys.exit()


def save_feed_into_cache(item):
    """
    This function saves feed item to file in json format.
    Name of file is date.
    File stores list which contains feed items related to certain date.
    If file does not exists, this function creates it.
    :param item: feed item
    """
    date = time.strftime('%Y%m%d', item.date)
    dir_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + 'feed_cache' + os.path.sep
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path = dir_path + date + '.json'
    item_to_cache = json.dumps(item._asdict(), ensure_ascii=False)
    if not os.path.exists(file_path):
        with open(file_path, 'a', encoding='utf-8') as fp:
            feed_list = [item_to_cache]
            json.dump(feed_list, fp)
    else:
        write_into_file(item_to_cache, file_path)


def write_into_file(item, path):
    """
    Save news item into cache if news item wasn't been cached earlier
    :param item: news item
    :param path: path to cache file
    """
    feed_list = check_if_cached(item, path)
    if feed_list:
        feed_list.append(item)
        with open(path, 'w', encoding='utf-8') as fp:
            json.dump(feed_list, fp)


def check_if_cached(item, path):
    """
    Check if news item was cached earlier
    :param item: news item
    :param path: path to cache file
    :return: list with cached news items to append it with new news
    """
    with open(path, encoding='utf-8') as fp:
        feed_list = json.load(fp)
        if item not in feed_list:
            return feed_list


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


def check_if_date_correct(date):
    """
    Check if parsed date correct
    :param date: date to check
    :return: None if date is correct, exit, if date is not correct
    """
    try:
        parse(date)
        return True
    except ValueError:
        print(f'You input incorrect date: {date}, please follow format yyyymmdd')
        return sys.exit()
