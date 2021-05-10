"""This module contains a class that represents a feed item"""

from datetime import datetime

from bs4 import BeautifulSoup
from dateutil.parser import parse


class News:
    """This class represents a feed item"""

    def __init__(self, feed_title, item):
        """This class constructor initializes the required variables for the news class"""
        self.feed_title = feed_title
        self.item = item
        self.links = {}
        self.title = self.item.title.text
        self.link = self.item.link.text
        self.description = self.__parse_description()
        self.date = self.__parse_date()

    def __parse_description(self):
        """
        This method parses the description of the feed item and formats it
        :return: str
        """
        if self.item.description:
            soup = BeautifulSoup(self.item.description.text, 'html.parser')
            images = soup.find_all('img')
            for image in images:
                item_position = len(self.links)
                self.links[item_position] = {'type': 'image', 'url': image['src'], 'attributes': {'alt': image['alt']}}
                image.replace_with(f'[image {item_position}{": " + image["alt"] + "] " if image["alt"] else "] "}')
            return soup.text

    def __parse_date(self):
        """
        This method parses the publication date of the feed item and formats it
        :return: str
        """
        if self.item.pubDate:
            date = self.item.pubDate.text
            return datetime.strftime(parse(date), '%a, %d %b %G %X')
        elif self.item.published:
            date = self.item.published.text
            return datetime.strftime(parse(date), '%a, %d %b %G %X')

    def __format_links(self):
        """
        This method returns the formatted links contained in the feed item
        :return: str
        """
        return '\n' + '\n'.join(f'[{position}] {link["url"]} ({link["type"]})' for position, link in self.links.items())

    def to_dict(self):
        """
        This method returns a dictionary representation of the news object
        :return: dict
        """
        return {'title': self.title,
                'url': self.link,
                'description': self.description,
                'date': self.date,
                'links': self.links if self.links else None}

    def __str__(self):
        """
        This method override default __str__ method which computes the string representation of an object
        :return: str
        """
        return f'[{self.feed_title}] {self.title}\n' \
               f'Date: {self.date}\n' \
               f'Link: {self.link}\n\n' \
               f'{self.description if self.description else ""}\n\n' \
               f'{"Links:" + self.__format_links() if self.links else ""}'.rstrip()
