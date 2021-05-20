'''This module contains a class which parse and print data'''
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
import json


class RssParser():
    '''This class parse the RSS feed and print data'''
    def __init__(self, doc, arg, logging):
        self.doc = doc
        self.arg = arg
        self.news = dict()
        self.logging = logging
        self.format_news()

    def format_news(self):
        '''This method collect all data in a dict'''
        self.logging.info('Collect all news and print')
        for num, item in enumerate(self.get_news()):
            if self.arg.json:
                self.news[num] = self.json_format(item)
            else:
                self.default_format(item)
        self.print_news()

    def print_news(self):
        '''This method print data JSON style'''
        if self.news:
            print(json.dumps(self.news, indent=4, sort_keys=False, default=str))

    def get_news(self):
        '''This method find data in xml file'''
        self.soup = BeautifulSoup(self.doc.content, 'lxml-xml')
        self.data = self.soup.findAll('item', limit=self.arg.limit)
        for item in self.data:
            news_data = dict()
            for tag in ['title', 'link']:
                news_data[tag] = item.find(tag).get_text()

            news_data['pubDate'] = date_parser.parse(item.find('pubDate').get_text())
            media = item.find('media:content')

            if media:
                news_data['media'] = media.get('url')
            else:
                news_data['media'] = None

            yield news_data

    def json_format(self, data):
        '''This method format data from xml file JSON style'''
        return {
            'Title': data['title'],
            'Publication date': data['pubDate'],
            'News link': data['link'],
            'Image link': data['media'],
            }

    def default_format(self, data):
        '''This method format data from xml file default style'''
        print('\n\n\nTitle: {0}\nDate: {1}\nLink: {2}\n\nImages links: {3}'.format(
                                                                            data['title'],
                                                                            data['pubDate'],
                                                                            data['link'],
                                                                            data['media'],))
