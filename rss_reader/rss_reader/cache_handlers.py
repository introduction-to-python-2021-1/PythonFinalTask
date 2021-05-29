"""
This module provides tools for working with cache
"""


import os
import json
import time
from rss_reader import str_funcs


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


def print_cached_feed(feed_list):
    """
    Makes readable str containing news
    :param feed_list: List with news to be shown
    :return: String with news
    """
    result_str = ''
    for feed in feed_list:
        loaded_feed = json.loads(feed)
        result_str = (f'Title: {loaded_feed["title"]}\nLink: {loaded_feed["link"]}\n'
                      f'Date: {time.strftime("%y-%m-%d %H:%M", tuple(loaded_feed["date"]))}\n')
        links = loaded_feed.get('links')
        result_str += str_funcs.get_links_as_str(links)
        content_list = loaded_feed.get('content')
        result_str += str_funcs.get_str_content(content_list)
        img = loaded_feed.get('img')
        result_str += str_funcs.get_img_as_str(img)
    return result_str


def save_feed_into_cache(item):
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
