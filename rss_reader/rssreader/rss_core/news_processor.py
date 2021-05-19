"""
    Module with class working with rss news
"""
from rssreader.rss_core.parser import Parser
from rssreader.rss_core.rss_classes import RSSNews
from rssreader.utils import util


class NewsProcessor:
    """

    Class for working with rss news
    """

    def __init__(self, parser: Parser, show_logs: bool = False):
        self.show_logs = show_logs
        self.parser = parser

    def get_news(self, link, news_count: int = None):
        """

        Function received data from site and creates RSS object based on this data

        :param link: link fo connection
        :param news_count: count of news which we want to get from site.
        If news_count = 0 - 0 news will received. For getting all news news_count mast have None value
        :return: RSSNews object
        """
        try:
            news_dict = self.parser.parse_news(link, news_count, show_logs=self.show_logs)
            rss_news = RSSNews(**news_dict)
            util.log(msg="RSSNews object was successfully created", flag="INFO", show_on_console=self.show_logs)
            return rss_news
        except (TypeError, AttributeError, ValueError) as err:
            util.log(flag="ERROR", show_on_console=True, msg=f"(NewsProcessor.get_news) {err.__class__} : {str(err)}")
