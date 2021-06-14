import json
import operator
from os.path import join

import rootpath
from dateutil.parser import parse


class Cache:
    """ Class for caching and retrieving cached news """

    def __init__(self, logger, file_name='cache.json'):
        self.__logger = logger
        self.file_name = file_name
        self.cache = self.__read_json()

    @property
    def file_path(self):
        """
        Getting the path to the file with the cache
        return: path
        """
        path = rootpath.detect()
        cache_file_path = join(path, 'rss_reader', 'data', 'cache', self.file_name)
        return cache_file_path

    @property
    def news_count(self):
        return len(self.cache)

    def __enter__(self):
        self.__logger.debug('News caching has started.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__write_to_json()
        self.__logger.debug('News caching has finished.')

    @staticmethod
    def __normalize_date(date):
        """
        Converting the date to the desired format
        :param date: date string representation
        """
        return parse(date, tzinfos={"EDT": -4 * 3600}).strftime('%Y%m%d')

    def __read_json(self):
        """
        Reading cached news from json file
        :return: news list
        """
        try:
            with open(self.file_path, 'r') as file:
                cache = json.load(file)
                return cache
        except FileNotFoundError as err:
            with open(self.file_path, 'w') as file:
                json.dump([], file)
                return []

    def __write_to_json(self):
        """
        Writing news to json file
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.cache, file, ensure_ascii=False, indent=3)

    def add_news_to_cache(self, news):
        """
        Adding news to the cache
        :param news: dictionary with news data

        """
        if news not in self.cache:
            self.cache.append(news)

    def get_from_cache(self, date, **kwargs):
        """
        Retrieving news from cache
        :param date: date string representation
        :param url: string representation of url
        :return: news list
        """
        pertinent_news = []

        if kwargs.get('url'):
            for onews in self.cache:
                if onews.get('date') and self.__normalize_date(onews['date']) == date and onews['url'] == kwargs.get(
                        'url'):
                    pertinent_news.append(onews)
        else:
            for onews in self.cache:
                if onews.get('date') and self.__normalize_date(onews['date']) == date:
                    pertinent_news.append(onews)

        if not pertinent_news:
            self.__logger.error('News not found.')
        else:
            self.__logger.debug('News received successfully.')
            return sorted(pertinent_news, key=operator.itemgetter('url', 'date'))
