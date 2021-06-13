import urllib

import feedparser


class RSSParser:
    """ Class describes parser object for rss """

    def __init__(self, url, logger, limit, ):
        self.__logger = logger
        self.url = url
        self.channel = self.get_rss_channel()
        self.limit = limit

    def get_rss_channel(self) -> feedparser:
        try:
            channel = feedparser.parse(self.url)
        except urllib.error.URLError:
            return ""
        if len(channel.entries) > 0:
            self.__logger.debug('Checking response body for the rss existing ended successfully')
            return channel
        else:
            self.__logger.debug('RSS does not detected in the response body')
            return ""

    def parse(self) -> dict:
        """ Function parses channel and packs it into the dictionary. """
        self.__logger.debug('RSS Channel parsing started')
        self.__logger.debug(f'News limit is: {self.limit}')
        news_dict = dict()
        news = self.channel.entries
        if self.limit <= 0 or self.limit >= len(news):
            self.limit = len(news)
        for index in range(self.limit):
            news_dict[f'new {index}'] = dict()
            news_dict[f'new {index}']['feed'] = self.channel['feed']['title']
            news_dict[f'new {index}']['title'] = news[index].title
            news_dict[f'new {index}']['date'] = news[index].published
            news_dict[f'new {index}']['link'] = news[index].link
            if news[index].get('description'):
                news_dict[f'new {index}']['description'] = news[index].description
            if news[index].get('links'):
                for link in enumerate(news[index].links):
                    news_dict[f'new {index}']['links'] = dict()
                    news_dict[f'new {index}']['links'][f'link {link[0]}'] = dict()
                    news_dict[f'new {index}']['links'][f'link {link[0]}']['href'] = link[1].href
                    news_dict[f'new {index}']['links'][f'link {link[0]}']['type'] = link[1].type
        self.__logger.debug('RSS Channel parsing ended')
        return news_dict
