import urllib

import feedparser
import requests
from requests.exceptions import ConnectionError, MissingSchema, InvalidSchema


class RssUrlValidator:
    """ THIS CLASS DESCRIBES URL VALIDATION LOGIC"""

    def __init__(self, url, logger):
        self.__url = url
        self.__logger = logger

    def get_status_code(self) -> int:
        """ FUNCTION RETURNS REQUEST STATUS CODE"""
        try:
            request = requests.get(self.__url).status_code
            return request
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
        try:
            d = feedparser.parse(f'{self.__url}')
        except urllib.error.URLError:
            return False
        if len(d['entries']) > 0:
            self.__logger.debug('Checking response body for the rss existing ended successfully')
            return True
        else:
            self.__logger.debug('RSS does not detected in the response body')
            return False

    def get_validated_url(self) -> str:
        """ FUNCTION RETURNS VALIDATED URL"""
        if self.validate_for_rss():
            return self.__url
        else:
            return ""
