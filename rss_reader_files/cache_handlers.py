import os
import json
import time


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