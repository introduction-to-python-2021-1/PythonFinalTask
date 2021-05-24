import requests
from feedparser import parse
from requests.exceptions import RequestException


class Connector:

    def __init__(self, url, logger):
        self.url = url
        self.__logger = logger
        self.response_text = None
        self.is_connect = self.is_connect()

    def is_connect(self):
        """
        Server connection check
        :return: boolean value
        """
        self.__logger.debug('Checking the connection to the server...')
        try:
            resp = requests.get(self.url)
            resp.raise_for_status()
            self.__logger.debug('Connection detected.')

            if len(parse(resp.text)['entries']) == 0:
                self.__logger.error('Invalid URL. RSS feed not found.')
                return False
            else:
                self.response_text = resp.text
                return True

        except RequestException:
            self.__logger.error(f'Connection not detected.')
            return False
