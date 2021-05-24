import re

from feedparser import parse


class RSSparser:
    LINK_TYPES = {
        'text/html': 'link',
        'image/jpeg': 'image',
        'image/png': 'image',
        'image/gif': 'gif',
        'video/mp4': 'video',
    }

    def __init__(self, source, logger, limit=False):
        self.__logger = logger
        self.__rss = parse(source)
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

        for i in range(self.limit):
            feed_data = dict()
            feed_data['feed'] = self.heading
            feed_data['title'] = self.news[i].get('title')
            feed_data['link'] = self.news[i].get('link')
            feed_data['date'] = self.news[i].get('published')

            if self.news[i].get('description'):
                feed_data['description'] = self.clean_text(self.news[i].get('description'))

            feed_links = self.news[i].get('links')
            if feed_links:
                list_of_links = [{'link': link.get('href'), 'type': self.LINK_TYPES.get(link.get('type'))} for link in
                                 feed_links]
                feed_data['links'] = list_of_links

            parsed_news.append(feed_data)

        self.__logger.debug('Parsing of the RSS feed finished.')

        return parsed_news
