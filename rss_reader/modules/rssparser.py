import re

from feedparser import parse

from modules.cache import Cache


class RSSparser:
    """ Class for parsing RSS feed """

    LINK_TYPES = {
        'text/html': 'link',
        'image/jpeg': 'image',
        'image/png': 'image',
        'image/gif': 'gif',
        'video/mp4': 'video',
    }

    def __init__(self, source, url, logger, limit=False):
        self.__logger = logger
        self.__cache = Cache(logger=self.__logger)
        self.__rss = parse(source)
        self.url = url
        self.limit = self.__validate_limit(limit)

    @property
    def heading(self):
        return self.__rss.feed.get('title')

    @property
    def news(self):
        return self.__rss.get('entries')

    @property
    def news_count(self):
        return len(self.news)

    def __validate_limit(self, limit):
        """
        Validation a given limit
        :param limit: given limit
        :return: validated limit
        """
        if limit <= 0 or limit > self.news_count:
            return self.news_count
        else:
            self.__logger.debug('Limit on the number of news: {}.'.format(limit))
            return limit

    @staticmethod
    def clean_text(text):
        """
        Parsing html tags
        :param text: string with html tags
        :return: string without html tags
        """
        cleaned = re.sub(r'<.*?>', '', text)  # remove html
        cleaned = cleaned.replace('&lt;', '<').replace('&gt;', '>')
        cleaned = cleaned.replace('&quot;', '"')
        cleaned = cleaned.replace('&rsquo;', "'")
        cleaned = cleaned.replace('&nbsp;', ' ')
        return cleaned

    def parse_news(self):
        """
        Parsing RSS feed
        :return: list of news
        """
        self.__logger.debug('Parsing of the RSS feed started...')
        parsed_news = []

        with self.__cache as cache:
            for onews in self.news:
                feed_data = dict()
                feed_data['url'] = self.url
                feed_data['feed'] = self.heading
                feed_data['title'] = onews.get('title')
                feed_data['link'] = onews.get('link')
                feed_data['date'] = onews.get('published')

                if onews.get('description'):
                    feed_data['description'] = self.clean_text(onews.get('description'))

                feed_links = onews.get('links')
                if feed_links:
                    list_of_links = [{'link': link.get('href'), 'type': self.LINK_TYPES.get(link.get('type'))} for link
                                     in
                                     feed_links]
                    feed_data['links'] = list_of_links

                parsed_news.append(feed_data)
                cache.add_news_to_cache(feed_data)

        self.__logger.debug('Parsing of the RSS feed finished.')

        return parsed_news[:self.limit]
