"""
    Module with class working with rss news
"""
from xhtml2pdf import pisa
from rss_core.cacher import Cacher
from rss_core.converter import RssConverter
from rss_core.parser import Parser
from rss_core.rss_classes import RssNews
from utils import util
from sys import exit


class NewsProcessor:
    """
    Class for working with rss news
    """

    def __init__(self, parser: Parser, cacher: Cacher = None, converter: RssConverter = None, show_logs: bool = False):
        self.show_logs = show_logs
        self.parser = parser
        self.cacher = cacher
        self.converter = converter
        self.news = []

    def load_news(self, link, cache_is_on: bool = True):
        """
        Function received data from site and creates RssNews object based on this data

        :param cache_is_on: whether we should cache our news into db
        :param link: link fo connection
        :return: None
        """
        if not self.parser:
            raise ValueError("Parser is not initialized")
        try:
            news_dict = self.parser.parse_news(link, show_logs=self.show_logs)
            rss_news = RssNews(**news_dict)
            if cache_is_on:
                if not self.cacher:
                    util.log(msg="Cacher is not initialized. Cache won't be create!", flag="WARNING",
                             show_on_console=True)
                else:
                    self.cacher.cache_rss_news(rss_news, link, show_logs=self.show_logs)
            util.log(msg="News was successfully loaded", flag="INFO", show_on_console=self.show_logs)
            self.news.append(rss_news)
        except (TypeError, AttributeError, ValueError) as err:
            util.log(flag="ERROR", show_on_console=True, msg=str(err))
            exit(1)

    def restore_news_from_cache(self, date: str, source_link: str = ""):
        """
        Restore news from db for given date and source link (if specified)
        :param date: date of news to be restored
        :param source_link:link of rss source of news to be restored
        :return: None
        """
        self.news = self.cacher.load_from_cache(source_link, date, self.show_logs)

    def get_news_as_json(self, news_limit: int = None):
        """
        Return json of loaded news news
        :param news_limit: count of news to be shown
        :return: dict
        """
        util.log(msg="Start converting news to json format...", flag="INFO", show_on_console=self.show_logs)
        limit_counter = news_limit
        channels_news = []
        for rss_news_item in self.news:
            if news_limit and limit_counter <= 0:
                break
            tmp_limit = min(limit_counter, len(rss_news_item.news)) if news_limit else news_limit
            channels_news.append(rss_news_item.as_json(limit=tmp_limit))
            if news_limit:
                limit_counter -= tmp_limit
        util.log(msg="News was converted successfully", flag="INFO", show_on_console=self.show_logs)

        return channels_news

    def get_news_as_str(self, news_limit: int = None):
        """
        Return string of loaded news news
        :param news_limit: count of news to be shown
        :return: str of news
        """
        util.log(msg="Start converting news str format...", flag="INFO", show_on_console=self.show_logs)
        str_news = ""
        limit_counter = news_limit
        for rss_news_item in self.news:
            if news_limit and limit_counter <= 0:
                break
            tmp_limit = min(limit_counter, len(rss_news_item.news)) if news_limit else news_limit
            str_news += rss_news_item.as_str(limit=tmp_limit) + "\n\n"
            if tmp_limit:
                limit_counter -= tmp_limit
        util.log(msg="News was converted successfully", flag="INFO", show_on_console=self.show_logs)
        return str_news

    def save_news_as_html(self, target_file: str, news_limit: int = None):
        """
        Dump loaded news into html file
        :param target_file: file for writing
        :param news_limit: count of news to be showen
        :return: None
        """
        if not target_file.endswith(".html"):
            raise ValueError("File for writing news as html should ends with '.html'")
        try:
            util.log(msg="Start creating html file...", flag="INFO", show_on_console=self.show_logs)
            util.log(msg=f"Checking directory for {target_file}...", flag="INFO", show_on_console=self.show_logs)
            util.create_directory(target_file)
            util.log(msg="Directory is OK", flag="INFO", show_on_console=self.show_logs)
            page = self.converter.get_news_template(rss_news=self.get_news_as_json(news_limit),
                                                    show_logs=self.show_logs)
            util.log(msg="Start writing data into file", flag="INFO", show_on_console=self.show_logs)
            with open(target_file, "w", encoding='utf-8') as fh:
                fh.write(page)
            util.log(msg=f"{target_file} was created", flag="INFO", show_on_console=self.show_logs)
        except OSError as err:
            util.log(msg=f"Error has occurred while converting news to html: {str(err)} ", flag="ERROR",
                     show_on_console=True)

    def save_news_as_pdf(self, target_file, news_limit: int = None):
        if not target_file.endswith(".pdf"):
            raise ValueError("File for writing news as pdf should ends with '.pdf'")
        try:
            util.log(
                msg="Start creating pdf file...",
                flag="INFO", show_on_console=self.show_logs)
            util.log(msg=f"Checking directory for {target_file}...", flag="INFO", show_on_console=self.show_logs)
            util.create_directory(target_file)
            util.log(msg="Directory is OK", flag="INFO", show_on_console=self.show_logs)
            page = self.converter.get_news_template(rss_news=self.get_news_as_json(news_limit),
                                                    show_logs=self.show_logs)
            util.log(msg="Start writing data into file", flag="INFO", show_on_console=self.show_logs)
            with open(target_file, "w+b") as resultFile:
                pisa.CreatePDF(page, dest=resultFile)
            util.log(msg=f"{target_file} was created", flag="INFO", show_on_console=self.show_logs)
        except OSError as err:
            util.log(msg=f"Error has occurred while converting news to html: {str(err)} ", flag="ERROR",
                     show_on_console=True)
