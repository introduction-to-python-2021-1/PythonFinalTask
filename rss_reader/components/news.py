"""This module contains a class that represents a feed item"""

from datetime import datetime
import os
import json

from bs4 import BeautifulSoup
from dateutil.parser import parse


class News:
    """This class represents a feed item"""

    def __init__(self, feed_title, item, source, logger):
        """This class constructor initializes the required variables for the news class"""
        self.feed_title = feed_title
        self.item = item
        self.source = source
        self.logger = logger
        if isinstance(self.item, dict):
            self.__from_cache()
        else:
            self.links = {}
            self.title = self.item.title.text
            self.link = self.item.link.text
            self.description = self.__parse_description()
            self.date = self.__parse_date()
            self.formatted_date = datetime.strftime(self.date, '%a, %d %b %G %X')
            self.__cache_news()

    def __parse_description(self) -> str:
        """This method parses the description of the feed item and formats it"""
        if self.item.description:
            soup = BeautifulSoup(self.item.description.text, 'html.parser')
            images = soup.find_all('img')
            for image in images:
                item_position = len(self.links)
                self.links[item_position] = {'type': 'image', 'url': image['src'], 'attributes': {'alt': image['alt']}}
                image.replace_with(f'[image {item_position}{": " + image["alt"] + "] " if image["alt"] else "] "}')
            return soup.text

    def __parse_date(self) -> datetime:
        """This method parses the publication date of the feed item"""
        if self.item.pubDate:
            date = self.item.pubDate.text
            return parse(date)
        elif self.item.published:
            date = self.item.published.text
            return parse(date)

    def __format_links(self) -> str:
        """This method returns the formatted links contained in the feed item"""
        return '\n' + '\n'.join(f'[{position}] {link["url"]} ({link["type"]})' for position, link in self.links.items())

    def to_dict(self) -> dict:
        """This method returns a dictionary representation of the news object"""
        return {'title': self.title,
                'url': self.link,
                'description': self.description,
                'date': self.formatted_date,
                'links': self.links if self.links else None}

    def __str__(self) -> str:
        """This method override default __str__ method which computes the string representation of an object"""
        return f'[{self.feed_title}] {self.title}\n' \
               f'Date: {self.formatted_date}\n' \
               f'Link: {self.link}\n\n' \
               f'{self.description if self.description else ""}\n\n' \
               f'{"Links:" + self.__format_links() if self.links else ""}'.rstrip()

    def __cache_news(self):
        """This method caches the news"""
        cache_folder_path = 'cache' + os.path.sep
        cache_date = datetime.strftime(self.date, "%Y%m%d")
        cache_file_path = f'{cache_folder_path}{cache_date}.json'
        source_feed_already_cached = False
        news_already_cached = False
        source_feed_index = None
        source_feed_cached_news_number = None
        if not os.path.exists(cache_folder_path):
            os.mkdir(cache_folder_path)
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as file:
                cached_data = json.load(file)
            for cached_feed_index, cached_feed in cached_data.items():
                if cached_feed['source'] == self.source:
                    source_feed_already_cached = True
                    source_feed_index = cached_feed_index
                    for cached_news in cached_feed['items'].values():
                        if cached_news['url'] == self.link:
                            news_already_cached = True
                            break
                    if not news_already_cached:
                        source_feed_cached_news_number = len(cached_feed['items'])
                if news_already_cached or source_feed_already_cached:
                    break
            if not news_already_cached:
                self.logger.info(' Caching news')
                if source_feed_already_cached:
                    cached_data[source_feed_index]['items'][source_feed_cached_news_number] = self.to_dict()
                else:
                    cached_data[len(cached_data)] = {'title': self.feed_title,
                                                     'source': self.source,
                                                     'items': {
                                                         0: self.to_dict()
                                                     }}
                with open(cache_file_path, 'w') as file:
                    json.dump(cached_data, file, indent=4, ensure_ascii=False)
        else:
            with open(cache_file_path, 'w') as file:
                json.dump({0: {'title': self.feed_title,
                               'source': self.source,
                               'items': {
                                   0: self.to_dict()
                               }}}, file, indent=4, ensure_ascii=False)

    def __from_cache(self):
        """This method retrieves news variables from cached news"""
        self.links = self.item['links']
        self.title = self.item['title']
        self.link = self.item['url']
        self.description = self.item['description']
        self.formatted_date = self.item['date']
