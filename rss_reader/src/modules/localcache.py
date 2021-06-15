import os.path
import json
from dateutil.parser import parse
from src import rss_reader
from copy import deepcopy


class Cache:
    __root_path = os.path.dirname(rss_reader.__file__) + '/localcache/cached_news.json'

    def __init__(self, logger, date=None, source=None):
        self.cached_data = self.get_cached_news()
        self.date = date
        self.source = source
        self.__filename = 'cached_news.json'
        self.__logger = logger

    def cache_news(self, data) -> None:
        self.__logger.debug('Started caching news')
        link = data['new 0']['link'].split('/', 3)[2]

        date = parse(data['new 0']['date'], tzinfos={'EDT': -4 * 3600}).strftime('%Y%m%d')
        if not self.cached_data.get(link):
            self.cached_data[link] = dict()

        if not self.cached_data[link].get(date):
            self.cached_data[link][date] = list()

        if len(self.cached_data[link][date]) == 0:
            self.cached_data[link][date].append(data)
        else:
            for news in self.cached_data[link][date]:
                cache_values = news.values()
                data_values = data.values()
                for data_news in data_values:
                    for cached_news in cache_values:
                        if data_news.get(link) == cached_news.get(link):
                            pass
                        else:
                            self.cached_data[link][date].append(data)

        with open(self.__root_path, 'w+') as file:
            file.write(json.dumps(self.cached_data, indent=2, ensure_ascii=False))
        self.__logger.debug('Ended caching news')

    def get_from_cached_news(self) -> dict:
        news_list = list()
        if self.date is not None:

            date = parse(self.date, tzinfos={'EDT': -4 * 3600}).strftime('%Y%m%d')
            if self.source is not None:

                if self.cached_data[self.source.split('/', 3)[2]].get(date):

                    return self.cached_data[self.source.split('/', 3)[2]].get(date)
                else:
                    print('No cached news for this date')
            else:
                for news in self.cached_data:
                    if news.get(date):
                        news_list.append(news)
        else:
            print('No date')

    def get_cached_news(self) -> dict:
        try:
            open(self.__root_path, 'r')
        except FileNotFoundError:
            with open(self.__root_path, 'w') as file:
                file.write('{}')
        finally:
            with open(self.__root_path, 'r') as file:
                return json.load(file)
