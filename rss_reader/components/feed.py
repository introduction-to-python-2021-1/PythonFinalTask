"""This module contains a class that represent a feed"""

import json
import os
import sys

from components.news import News


class Feed:
    """This class represents a feed"""

    def __init__(self, source, date, limit, to_json, logger, feed_title=None, items=None):
        """
        This class constructor initializes the required variables for the feed class
        and calls the method that creates news objects and adds them to news list
        """
        self.limit = limit
        self.to_json = to_json
        self.logger = logger
        self.date = date
        self.source = source
        self.news_list = []
        if self.date:
            self.cached_feeds = {}
            self.__create_feed_from_cache()
        else:
            self.feed_title = feed_title
            self.items = items
            self.__create_feed()

    def __create_feed(self):
        """This method creates news objects and adds them to the news list"""
        self.logger.info(' Preparing a feed')
        for item in self.items:
            self.news_list.append(News(self.feed_title, item, self.source, self.logger))

    def __create_feed_from_cache(self):
        """
        This method get feed in json format from the cache, get news in json format from it, creates news objects
        and adds them to the cached news dict
        """
        self.logger.info(' Trying to get news from cache')
        cache_folder_path = 'cache' + os.path.sep
        cache_file_path = f'{cache_folder_path}{self.date}.json'
        temp_feed = None
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as file:
                cached_data = json.load(file)
            for cached_feed in cached_data.values():
                if self.source and cached_feed['source'] != self.source:
                    continue
                else:
                    for cached_news in cached_feed['items'].values():
                        if len(self.news_list) == self.limit:
                            break
                        else:
                            news = News(cached_feed['title'], cached_news, cached_feed['source'], self.logger)
                            self.news_list.append(news)
                            if temp_feed is None:
                                temp_feed = {'title': news.feed_title,
                                             'source': news.source,
                                             'items': {
                                                 0: news.to_dict()
                                             }}
                            else:
                                temp_feed['items'][len(temp_feed['items'])] = news.to_dict()
                if temp_feed:
                    self.cached_feeds[len(self.cached_feeds)] = temp_feed
                    temp_feed = None
                if len(self.news_list) == self.limit:
                    break
            if self.source and not self.news_list:
                self.logger.error(f' Cache for date "{self.date}" and source URL "{self.source}" was not found')
                sys.exit()
            self.logger.info(f' Retrieved {len(self.news_list)} news from cache')
        else:
            self.logger.error(f' Cache for date "{self.date}" was not found')
            sys.exit()

    def __str__(self) -> str:
        """This method override default __str__ method which computes the string representation of an object"""
        if self.to_json:
            if self.date:
                self.logger.info(' Printing news to STDOUT in JSON')
                return json.dumps(self.cached_feeds, indent=4, ensure_ascii=False)
            else:
                self.logger.info(' Printing news to STDOUT in JSON')
                return json.dumps({0: {'title': self.feed_title,
                                       'source': self.source,
                                       'items': {
                                           index: news.to_dict() for index, news in
                                           enumerate(self.news_list[:self.limit])
                                       }}}, indent=4, ensure_ascii=False)
        else:
            self.logger.info(' Printing news to STDOUT')
            return '\n\n'.join(str(news) for news in self.news_list[:self.limit])
