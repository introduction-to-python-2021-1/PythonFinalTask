import feedparser


class RSSParser:
    """ CLASS DESCRIBES PARSER OBJECT FOR RSS """

    def __init__(self, url, logger, limit, ):
        self.channel = feedparser.parse(url)
        self.limit = limit
        self.__logger = logger

    def get_channel_title(self) -> str:
        """ FUNCTION RETURNS TITLE OF THE CURRENT RSS CHANNEL """
        return self.channel['feed']['title']

    def parse(self) -> dict:
        """ FUNCTION PARSES CHANNEL AND PACK IT INTO THE DICTIONARY"""
        self.__logger.debug('RSS Channel parsing started')
        self.__logger.debug(f'News limit is: {self.limit}')
        news_dict = dict()
        news = self.channel.entries
        if self.limit <= 0 or self.limit >= len(news):
            self.limit = len(news)
        for i in range(self.limit):
            news_dict[f'new {i}'] = dict()
            news_dict[f'new {i}']['feed'] = self.get_channel_title()
            news_dict[f'new {i}']['title'] = news[i].title
            news_dict[f'new {i}']['date'] = news[i].published
            news_dict[f'new {i}']['link'] = news[i].link
            if news[i].get('description'):
                news_dict[f'new {i}']['description'] = news[i].description
            if news[i].get('links'):
                for link in enumerate(news[i].links):
                    news_dict[f'new {i}']['links'] = dict()
                    news_dict[f'new {i}']['links'][f'link {link[0]}'] = dict()
                    news_dict[f'new {i}']['links'][f'link {link[0]}']['href'] = link[1].href
                    news_dict[f'new {i}']['links'][f'link {link[0]}']['type'] = link[1].type
        self.__logger.debug('RSS Channel parsing ended')
        return news_dict
