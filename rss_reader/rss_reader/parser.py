from dateutil.parser import parse
from termcolor import colored


class RssParser:
    """This class parse the RSS feed and print data
        soup (bs4.BeautifulSoup): Object of class bs4.BeautifulSoup containing data from xml file
    """
    def __init__(self, soup):
        self.soup = soup

    def select_news(self):
        """This method find data in xml file"""
        data = self.soup.findAll('item')
        for item in data:
            news_data = dict()
            for tag in ['title', 'link']:
                news_data[tag] = item.find(tag).get_text()

            news_data['pubDate'] = parse(item.find('pubDate').get_text())
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
            'Title': data["title"],
            'Publication date': data['pubDate'],
            'News link': data['link'],
            'Image link': data['media'],
        }

    @staticmethod
    def default_format(data, color):
        """This method format data from xml file default style"""
        if color:
            out = '\n\n\nTitle: {0}\nDate: {1}\nLink: {2}\n\nImages links: {3}'.format(
                                                                                    colored(data['title'], 'green'),
                                                                                    data['pubDate'],
                                                                                    colored(data['link'], 'blue'),
                                                                                    colored(data['media'], 'blue'),)
        else:
            out = '\n\n\nTitle: {0}\nDate: {1}\nLink: {2}\n\nImages links: {3}'.format(
                                                                                    data['title'],
                                                                                    data['pubDate'],
                                                                                    data['link'],
                                                                                    data['media'],)
        return out
