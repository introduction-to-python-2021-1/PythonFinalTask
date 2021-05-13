import os
from datetime import datetime
import json
import sys

from components.news import News


class Cache:
    def __init__(self, logger):
        """This class constructor initializes the required variables for the news class"""
        self.logger = logger
        self.cache_folder_path = 'cache' + os.path.sep
        if not os.path.exists(self.cache_folder_path):
            os.mkdir(self.cache_folder_path)

    def cache_news(self, news):
        """This method prepares data for writing to the cache file"""
        cache_date = datetime.strftime(news.date, "%Y%m%d")
        cache_file_path = f'{self.cache_folder_path}{cache_date}.json'
        source_feed_already_cached = False
        news_already_cached = False
        source_feed_index = None
        source_feed_cached_news_number = None
        cached_data = self.__get_cached_data(cache_file_path)
        if cached_data:
            for cached_feed_index, cached_feed in cached_data.items():
                if cached_feed['source'] == news.source:
                    source_feed_already_cached = True
                    source_feed_index = cached_feed_index
                    for cached_news in cached_feed['items'].values():
                        if cached_news['url'] == news.link:
                            news_already_cached = True
                            break
                    if not news_already_cached:
                        source_feed_cached_news_number = len(cached_feed['items'])
                if news_already_cached or source_feed_already_cached:
                    break
            if not news_already_cached:
                if source_feed_already_cached:
                    cached_data[source_feed_index]['items'][source_feed_cached_news_number] = news.to_dict()
                else:
                    cached_data[len(cached_data)] = {'title': news.feed_title,
                                                     'source': news.source,
                                                     'items': {
                                                         0: news.to_dict()
                                                     }}
                self.__write_cache(cache_file_path, cached_data)
        else:
            data = {0: {'title': news.feed_title,
                        'source': news.source,
                        'items': {
                            0: news.to_dict()
                        }}}
            self.__write_cache(cache_file_path, data)

    def __get_cached_data(self, cache_file_path):
        """
        This method fetches the cache from the cache file

        Returns:
            dict: Dictionary that contain cached feed
            None: If the cache file is corrupted, empty or does not exist
        """
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as file:
                try:
                    cached_data = json.load(file)
                    return cached_data
                except json.JSONDecodeError:
                    self.logger.error(f' Unable to parse JSON from "{cache_file_path}". '
                                      f'This file is corrupted or empty and will be deleted.')
                    os.remove(cache_file_path)
        return None

    def __write_cache(self, cache_file_path, data):
        """This method writes the cache to the cache file"""
        self.logger.info(' Caching news')
        with open(cache_file_path, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_news_from_cache(self, date, limit, source) -> (list, dict):
        """
        This method get news in json format from cached data, creates news objects and returns cached feeds dict
        and news list
        """
        self.logger.info(' Trying to get news from cache')
        cache_file_path = f'{self.cache_folder_path}{date}.json'
        temp_feed = None
        news_list = []
        cached_feeds = {}
        cached_data = self.__get_cached_data(cache_file_path)
        if cached_data:
            for cached_feed in cached_data.values():
                if source and cached_feed['source'] != source:
                    continue
                else:
                    for cached_news in cached_feed['items'].values():
                        if len(news_list) == limit:
                            break
                        else:
                            news = News(cached_feed['title'], cached_news, cached_feed['source'], self.logger)
                            news_list.append(news)
                            if temp_feed is None:
                                temp_feed = {'title': news.feed_title,
                                             'source': news.source,
                                             'items': {
                                                 0: news.to_dict()
                                             }}
                            else:
                                temp_feed['items'][len(temp_feed['items'])] = news.to_dict()
                if temp_feed:
                    cached_feeds[len(cached_feeds)] = temp_feed
                    temp_feed = None
                if len(news_list) == limit:
                    break
            if source and not news_list:
                self.logger.error(f' Cache for date "{date}" and source URL "{source}" was not found')
                sys.exit()
            self.logger.info(f' Retrieved {len(news_list)} news from cache')
            return news_list, cached_feeds
        else:
            self.logger.error(f' Cache for date "{date}" was not found')
            sys.exit()
