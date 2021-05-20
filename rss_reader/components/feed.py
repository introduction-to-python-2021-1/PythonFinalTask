"""This module contains a class that represent a feed"""

import json

from components.news import News
from components.cache import Cache


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
            self.cache = Cache(self.logger)
            self.news_list, self.cached_feeds = self.cache.get_news_from_cache(self.date, self.limit, self.source)
        else:
            self.feed_title = feed_title
            self.items = items
            self.__create_feed()

    def __create_feed(self):
        """This method creates news objects and adds them to the news list"""
        self.logger.info(' Preparing a feed')
        for item in self.items:
            self.news_list.append(News(self.feed_title, item, self.source, self.logger))

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
