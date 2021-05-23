"""
    Module with class working with rss news
"""
from rss_core.parser import Parser
from rss_core.rss_classes import RssNews
from utils import util


class NewsProcessor:
    """
    Class for working with rss news
    """

    def __init__(self, parser: Parser, show_logs: bool = False):
        self.show_logs = show_logs
        self.parser = parser

    def get_news(self, link):
        """
        Function received data from site and creates RSS object based on this data

        :param link: link fo connection
        :return: RSSNews object
        """
        if not self.parser:
            raise ValueError("Parser is not initialized")
        try:
            news_dict = self.parser.parse_news(link, show_logs=self.show_logs)
            rss_news = RssNews(**news_dict)
            util.log(msg="RSSNews object was successfully created", flag="INFO", show_on_console=self.show_logs)
            return rss_news
        except (TypeError, AttributeError, ValueError) as err:
            util.log(flag="ERROR", show_on_console=True, msg=str(err))
            exit(1)
