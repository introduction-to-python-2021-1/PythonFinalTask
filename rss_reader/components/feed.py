"""This module contains a class that represent a feed"""

import json

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.data import JsonLexer

from components.news import News


class Feed:
    """This class represents a feed"""

    def __init__(self, source_url, news_limit, to_json, to_colorized_format, logger, feed_title, cache, news_items=None,
                 news_list=None):
        """
        This class constructor initializes the required variables for the feed class
        and calls the method that creates news objects and adds them to news list

        Parameters:
            source_url (str): Link to RSS Feed
            news_limit (int or NoneType): Value that limits the number of news
            to_json (bool): If True printing news in JSON format
            to_colorized_format (bool): If True colors the result
            logger (module): logging module
            feed_title (str): News feed title
            cache (Cache): Object of class Cache
            news_items (bs4.element.ResultSet): Object of class bs4.element.ResultSet containing news items
            news_list (list): List of objects of class News
        """
        self.logger = logger
        self.logger.info('Preparing a feed')
        self.news_limit = news_limit
        self.to_json = to_json
        self.to_colorized_format = to_colorized_format
        self.source_url = source_url
        self.feed_title = feed_title
        self.cache = cache
        if not news_list:
            self.news_list = []
            self.news_items = news_items
            self.__create_feed()
        else:
            self.news_list = news_list

    def __create_feed(self):
        """This method creates news objects and adds them to the news list"""
        for news_item in self.news_items:
            self.news_list.append(
                News(self.feed_title, news_item, self.source_url, self.logger, self.cache, self.to_colorized_format))

    def __str__(self) -> str:
        """This method override default __str__ method which computes the string representation of an object"""
        if self.to_json:
            self.logger.info('Printing news to STDOUT in JSON')
            formatted_json = json.dumps({0: {'title': self.feed_title,
                                             'source': self.source_url,
                                             'items': {
                                                 index: news.to_dict() for index, news in
                                                 enumerate(self.news_list[:self.news_limit])
                                             }}}, indent=4, ensure_ascii=False)
            if self.to_colorized_format:
                return highlight(formatted_json, JsonLexer(), TerminalFormatter())
            else:
                return formatted_json
        else:
            self.logger.info('Printing news to STDOUT')
            return '\n\n'.join(str(news) for news in self.news_list[:self.news_limit])
