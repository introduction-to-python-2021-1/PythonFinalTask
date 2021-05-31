from datetime import datetime


class RssParser:
    """This class parse the RSS feed and print data
        soup (bs4.BeautifulSoup): Object of class bs4.BeautifulSoup containing data from xml file
    """
    def __init__(self, soup):

        self.soup = soup

    def get_news(self):
        """This method find data in xml file"""
        data = self.soup.findAll('item')
        for item in data:
            news_data = dict()
            for tag in ['title', 'link']:
                news_data[tag] = item.find(tag).get_text()

            news_data['pubDate'] = datetime.strptime(item.
                                                     find('pubDate').get_text(),
                                                     '%Y-%m-%dT%H:%M:%SZ')
            media = item.find('media:content')

            if media:
                news_data['media'] = media.get('url')
            else:
                news_data['media'] = None

            yield news_data

    @staticmethod
    def json_format(data):
        """This method format data from xml file JSON style"""
        return {
            'Title': data['title'],
            'Publication date': data['pubDate'],
            'News link': data['link'],
            'Image link': data['media'],
            }

    @staticmethod
    def default_format(data):
        """This method format data from xml file default style"""
        return '\n\n\nTitle: {0}\nDate: {1}\nLink: {2}\n\nImages links: {3}'.format(
                                                                            data['title'],
                                                                            data['pubDate'],
                                                                            data['link'],
                                                                            data['media'],)
