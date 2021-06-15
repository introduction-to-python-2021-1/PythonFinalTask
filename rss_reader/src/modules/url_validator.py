import urllib

import feedparser
import requests
from feedparser import FeedParserDict
from requests.exceptions import ConnectionError, MissingSchema, InvalidSchema


class RssUrlManager:
    """ Class describes url validation logic"""

    def __init__(self, url, logger):
        self.__url = url
        self.__logger = logger

    def get_status_code(self) -> int:
        """ FUNCTION RETURNS REQUEST STATUS CODE"""
        try:
            status_code = requests.get(self.__url).status_code
            return status_code
        except ConnectionError:
            self.__logger.debug('Connection was not provided')
        except MissingSchema:
            self.__logger.debug('Invalid url')
        except InvalidSchema:
            self.__logger.debug('Invalid url')

    def validate_for_rss(self) -> bool:
        """ FUNCTION CHECKS REQUEST BODY FOR THE RSS DATA"""
        self.__logger.debug('Checking response body for the rss existing started')
        if self.get_status_code() == 200:
            self.__logger.debug('Request status code 200')
        else:
            self.__logger.debug(f'Invalid request')
            return False

        if self.get_rss_from_url().get('entries') and len(self.get_rss_from_url().entries) > 0:
            self.__logger.debug('Checking response body for the rss existing ended successfully')
            return True
        else:
            self.__logger.debug('RSS does not detected in the response body')
            print('RSS does not exists in the present url')
            return False

    def get_rss_from_url(self) -> FeedParserDict:
        try:
            channel = feedparser.parse(self.__url)
            return channel if len(channel.entries) > 0 else dict()
        except urllib.error.URLError:
            return FeedParserDict()

    def get_validated_url(self) -> str:
        """ FUNCTION RETURNS VALIDATED URL"""
        if self.validate_for_rss():
            return self.__url
        else:
            return ""
