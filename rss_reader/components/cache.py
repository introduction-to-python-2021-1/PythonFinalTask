"""This module contains a class containing methods for working with the cache"""

from datetime import datetime
import hashlib
import imghdr
import json
import os
import sys
import urllib.request

from components.feed import Feed
from components.news import News


class Cache:
    """This class is needed for caching news"""

    def __init__(self, logger):
        """
        This class constructor initializes the required variables for the caching

        Parameters:
            logger (module): logging module
        """
        self.logger = logger
        self.cache_folder_path = 'cache' + os.path.sep
        self.cache_images_folder_path = self.cache_folder_path + 'images' + os.path.sep
        if not os.path.exists(self.cache_images_folder_path):
            os.makedirs(self.cache_images_folder_path)

    def cache_news(self, news):
        """
        This method prepares data for writing to the cache file

        Parameters:
            news (News): Object of class News
        """
        cache_date = datetime.strftime(news.date, "%Y%m%d")
        cache_file_path = f'{self.cache_folder_path}{cache_date}.json'
        news_already_cached = False
        cached_data = self.__get_cached_data(cache_file_path)
        if cached_data:
            cached_feeds_sources = tuple((cached_feed['source'] for cached_feed in cached_data.values()))
            if news.source in cached_feeds_sources:
                source_feed_index = str(cached_feeds_sources.index(news.source))
                cached_news_links = tuple(
                    cached_news['url'] for cached_news in cached_data[source_feed_index]['items'].values())
                if news.link in cached_news_links:
                    news_already_cached = True
                else:
                    cached_data[source_feed_index]['items'][len(cached_news_links)] = news.to_dict()
            else:
                cached_data[len(cached_data)] = {'title': news.feed_title,
                                                 'source': news.source,
                                                 'items': {
                                                     0: news.to_dict()
                                                 }}
        else:
            cached_data = {0: {'title': news.feed_title,
                               'source': news.source,
                               'items': {
                                   0: news.to_dict()
                               }}}
        if not news_already_cached:
            self.__write_cache(cache_file_path, cached_data)
            self.__cache_images(news)

    def __get_cached_data(self, cache_file_path):
        """
        This method fetches the cache from the cache file

        Parameters:
            cache_file_path (str): Path to file with cache

        Returns:
            dict: Dictionary that contain cached feed
            None: If the cache file is corrupted, empty or does not exist
        """
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as file:
                try:
                    cached_data = json.load(file)
                    return cached_data
                except json.JSONDecodeError:
                    self.logger.error(f' Unable to parse JSON from "{cache_file_path}". '
                                      f'This file is corrupted or empty and will be deleted.')
                    os.remove(cache_file_path)
        return None

    def __write_cache(self, cache_file_path, data):
        """
        This method writes the cache to the cache file

        Parameters:
            cache_file_path (str): Path to file with cache
            data (dict): Dictionary with data to write to cache file
        """
        self.logger.info(' Caching news')
        with open(cache_file_path, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_news_from_cache(self, publication_date, source_url, news_limit, to_json) -> list:
        """
        This method get news in JSON format from cached data, creates news objects and returns cached feeds list

        Parameters:
            publication_date (str): Date of publication of the news in the format "%Y%m%d"
            news_limit (int or NoneType): Value that limits the number of news
            source_url (str): Link to the source from which the news was received
            to_json (bool): If True news will be printed in JSON format
        """
        self.logger.info(' Trying to get news from cache')
        cache_file_path = f'{self.cache_folder_path}{publication_date}.json'
        feeds_list = []
        retrieved_news_amount = 0
        date_object = datetime.strptime(publication_date, '%Y%m%d')
        cached_data = self.__get_cached_data(cache_file_path)
        if cached_data:
            for cached_feed in cached_data.values():
                if source_url and cached_feed['source'] != source_url:
                    continue
                feed_title = cached_feed['title']
                news_list = []
                for cached_news in cached_feed['items'].values():
                    if retrieved_news_amount != news_limit:
                        news = News(cached_feed['title'], cached_news, cached_feed['source'], self.logger)
                        news_list.append(news)
                        retrieved_news_amount += 1
                    else:
                        break
                feed = Feed(source_url, None, to_json, self.logger, feed_title, news_list=news_list)
                feeds_list.append(feed)
                if retrieved_news_amount == news_limit:
                    break
            if source_url and not feeds_list:
                self.logger.error(
                    f' Cache for published date "{date_object.date()}" and source URL "{source_url}" was not found')
                sys.exit()
            self.logger.info(f' Retrieved {retrieved_news_amount} news from cache')
            return feeds_list
        else:
            self.logger.error(f' No cached news found with published date {date_object.date()}')
            sys.exit()

    def __cache_images(self, news):
        """
        This method downloads images from URL and saves them

        Parameters:
            news (News): Object of class News
        """
        for link_index, link in news.links.items():
            if 'image' in link['type']:
                cached_image_filename = f'{hashlib.md5(news.link.encode()).hexdigest()}_{link_index}'
                cached_image_file_path = self.cache_images_folder_path + cached_image_filename
                urllib.request.urlretrieve(link['url'], cached_image_file_path)
                image_format = imghdr.what(cached_image_file_path)
                os.rename(cached_image_file_path, f'{cached_image_file_path}.{image_format}')
