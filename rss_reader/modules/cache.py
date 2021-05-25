import json
import operator

from dateutil.parser import parse


class Cache:
    def __init__(self, cache_file='cache.json', logger=None):
        self.__logger = logger
        self.cache_file_name = cache_file
        self.cache = self.__read_json()

    def __enter__(self):
        self.__logger.debug('News caching has started.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__write_to_json()
        self.__logger.debug('News caching has finished.')

    def __read_json(self):
        try:
            with open(self.cache_file_name, 'r') as file:
                cache = json.load(file)
                return cache
        except FileNotFoundError as err:
            with open(self.cache_file_name, 'w') as file:
                json.dump([], file)
                return []

    def add_news_to_cache(self, news):
        if news not in self.cache:
            self.cache.append(news)

    def __write_to_json(self):
        with open(self.cache_file_name, 'w', encoding='utf-8') as file:
            json.dump(self.cache, file, ensure_ascii=False, indent=3)

    @staticmethod
    def __normalize_date(date):
        return parse(date).strftime('%Y%m%d')

    def get_from_cache(self, date, url=None):
        pertinent_news = []
        if url:
            news = sorted(self.cache, key=operator.itemgetter('date', 'url'))
            for onews in news:
                if self.__normalize_date(onews['date']) == date and onews['url'] == url:
                    pertinent_news.append(onews)
        else:
            news = sorted(self.cache, key=operator.itemgetter('date'))
            for onews in news:
                if self.__normalize_date(onews['date']) == date:
                    pertinent_news.append(onews)
        if not pertinent_news:
            self.__logger.error('News not found.')
        else:
            return pertinent_news
