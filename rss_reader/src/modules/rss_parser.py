from src.modules.localcache import Cache


class RSSParser:
    """ Class describes parser object for rss """

    def __init__(self, channel, logger):
        self.__logger = logger
        self.channel = channel

    def parse(self) -> dict:
        """ Function parses channel and packs it into the dictionary. """
        self.__logger.debug('RSS Channel parsing started')
        news_dict = dict()
        for news in enumerate(self.channel.entries):
            news_dict[f'new {news[0]}'] = dict()
            news_dict[f'new {news[0]}']['feed'] = self.channel['feed']['title']
            news_dict[f'new {news[0]}']['title'] = news[1].title
            news_dict[f'new {news[0]}']['date'] = news[1].published
            news_dict[f'new {news[0]}']['link'] = news[1].link
            if news[1].get('description'):
                news_dict[f'new {news[0]}']['description'] = news[1].description
            if news[1].get('links'):
                for link in enumerate(news[1].links):
                    news_dict[f'new {news[0]}']['links'] = dict()
                    news_dict[f'new {news[0]}']['links'][f'link {link[0]}'] = dict()
                    news_dict[f'new {news[0]}']['links'][f'link {link[0]}']['href'] = link[1].href
                    news_dict[f'new {news[0]}']['links'][f'link {link[0]}']['type'] = link[1].type
        self.__logger.debug('RSS Channel parsing ended')
        Cache(self.__logger).cache_news(news_dict)
        return news_dict
