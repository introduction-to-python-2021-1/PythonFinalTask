import requests
from feedparser import parse
from requests.exceptions import RequestException


class Connector:

    def __init__(self, url, logger):
        self.url = url
        self.__logger = logger
        self.is_connected = self.__is_rss()

    def __str__(self):
        return self.is_connected

    def __is_connect(self):
        """
        Server connection check
        :return: boolean value
        """
        self.__logger.debug('Checking the connection to the server...')
        try:
            resp = requests.get(self.url)
            resp.raise_for_status()
            self.__logger.debug('Connection detected.')
            return True
        except RequestException:
            self.__logger.error(f'Connection not detected.')
            return False

    def __is_rss(self):
        """
        RSS feed check
        :return: boolean value
        """
        if self.__is_connect():
            if len(parse(self.url)['entries']) == 0:
                self.__logger.error('Invalid URL. RSS feed not found.')
                return False
            else:
                return True
        else:
            return False
