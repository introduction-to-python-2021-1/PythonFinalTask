"""This module contains a class that represent a feed"""

import json
from .news import News


class Feed:
    """This class represents a feed"""

    def __init__(self, feed_title, items, to_json, logger, limit):
        """This class constructor initializes the required variables for the feed class
        and calls the method that creates news objects and adds them to news list"""
        self.feed_title = feed_title
        self.limit = limit
        self.items = items[:self.limit]
        self.to_json = to_json
        self.logger = logger
        self.news_list = []
        self.__create_feed()

    def __create_feed(self):
        """
        This method creates news objects and adds them to the news list
        :return: None
        """
        self.logger.info(' Preparing a feed')
        for item in self.items:
            self.news_list.append(News(self.feed_title, item))

    def __str__(self):
        """
        This method override default __str__ method which computes the string representation of an object
        :return: str
        """
        if self.to_json:
            self.logger.info(' Printing news to STDOUT in JSON')
            return json.dumps({'title': self.feed_title,
                               'items': {
                                   index: news.to_dict() for index, news in enumerate(self.news_list)
                               }}, indent=4, ensure_ascii=False)
        else:
            self.logger.info(' Printing news to STDOUT')
            return '\n\n'.join(str(news) for news in self.news_list)
