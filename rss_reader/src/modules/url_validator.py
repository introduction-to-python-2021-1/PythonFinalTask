import requests
from requests.exceptions import ConnectionError, MissingSchema, InvalidSchema


class RssUrlValidator:
    """ Class describes url validation logic"""

    def __init__(self, url, logger):
        self.__url = url
        self.__logger = logger

    def get_status_code(self) -> int:
        """ Function returns request status code. """
        try:
            status_code = requests.get(self.__url).status_code
            return status_code
        except ConnectionError:
            self.__logger.debug('Connection was not provided')
        except MissingSchema:
            self.__logger.debug('Invalid url')
        except InvalidSchema:
            self.__logger.debug('Invalid url')

    def get_validated_url(self) -> str:
        """ Function returns validated url. """
        if self.get_status_code() == 200:
            return self.__url
        else:
            print('Invalid url')
            return ""
