"""
    Module with class working with rss news
"""
from rss_core.cacher import Cacher
from rss_core.parser import Parser
from rss_core.rss_classes import RssNews
from utils import util


class NewsProcessor:
    """
    Class for working with rss news
    """

    def __init__(self, parser: Parser, cacher: Cacher = None, show_logs: bool = False):
        self.show_logs = show_logs
        self.parser = parser
        self.cacher = cacher

    def get_news(self, link, cache_is_on: bool = True):
        """
        Function received data from site and creates RssNews object based on this data

        :param cache_is_on: whether we should cache our news into db
        :param link: link fo connection
        :return: RssNews object
        """
        if not self.parser:
            raise ValueError("Parser is not initialized")
        try:
            news_dict = self.parser.parse_news(link, show_logs=self.show_logs)
            rss_news = RssNews(**news_dict)
            if cache_is_on:
                if not self.cacher:
                    util.log(msg="Cacher is not initialized. Cash won't be create!", flag="WARNING",
                             show_on_console=True)
                else:
                    self.cacher.cache_rss_news(rss_news, link, show_logs=self.show_logs)
            util.log(msg="RssNews object was successfully created", flag="INFO", show_on_console=self.show_logs)
            return rss_news
        except (TypeError, AttributeError, ValueError) as err:
            util.log(flag="ERROR", show_on_console=True, msg=str(err))
            exit(1)
