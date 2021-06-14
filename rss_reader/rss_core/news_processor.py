"""
    Module with class working with rss news
"""
import os
import re
from jinja2 import Environment, FileSystemLoader

from xhtml2pdf import pisa
from rss_core.cacher import Cacher
from rss_core.parser import Parser
from rss_core.rss_classes import RssNews
from utils import util
from sys import exit

IMAGE_FOLDER = "/static/src/"
OUTPUT_FILE_NAME = "news_dump"


class NewsProcessor:
    """
    Class for working with rss news
    """

    def __init__(self, parser: Parser, cacher: Cacher = None, show_logs: bool = False):
        self.show_logs = show_logs
        self.parser = parser
        self.cacher = cacher
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

    def get_news_template(self, rss_news, img_files: dict, show_logs: bool = False):
        """
        Create html for saving into file

        :param img_files: dict of ig_link:src for inserting images into file
        :param rss_news: news to be inserted into template
        :param show_logs: show logs on console or not
        :return: str
        """
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('news_template.html')
        util.log(msg="Start rendering template...", flag="INFO", show_on_console=show_logs)
        generated_page = template.render(channels_news=rss_news, img_files=img_files)
        util.log(msg="Template was generated successfully", flag="INFO", show_on_console=show_logs)
        return generated_page

    def get_news_page(self, news_limit: int = None):
        """
        Prepare data and generate html page for given news
        :param news_limit: count of news to be shown
        :return: generated html page
        """
        news_for_printing = self.get_news_as_json(news_limit)
        img_files = self.cacher.get_images_from_db(news_for_restoring=news_for_printing)
        page = self.get_news_template(rss_news=news_for_printing,
                                      img_files=img_files,
                                      show_logs=self.show_logs)
        return page

    def save_news_as_html(self, output_to: str, news_limit: int = None):
        """
        Dump loaded news into html file
        :param output_to: file for writing
        :param news_limit: count of news to be shown
        :return: None
        """
        util.log(msg="Start creating html file...", flag="INFO", show_on_console=self.show_logs)
        try:
            target_file = self.check_target_output_file(output_to, "html")
            page = self.get_news_page(news_limit)
            util.log(msg="Start writing data into file", flag="INFO", show_on_console=self.show_logs)
            with open(target_file, "w", encoding='utf-8') as fh:
                fh.write(page)
            util.log(msg=f"{target_file} was created", flag="INFO", show_on_console=self.show_logs)
        except (OSError, ValueError) as err:
            util.log(msg=f"Error has occurred while converting news to html: {str(err)} ", flag="ERROR",
                     show_on_console=True)

    def check_target_output_file(self, output_to, file_format: str = ""):
        """
        Create dir for file, check if such a file is  already exist.
        If only path was specified(without file) then generate unique
        file name for this directory
        :param output_to: target directory with or without target file
        :param file_format: format of target file in case of necessity
        of generating unique file name
        :return: checked(or generated) file name with filepath to it
        """
        util.create_directory(output_to)
        if re.search(r'\.\w+$', output_to):
            if not output_to.endswith(file_format):
                raise ValueError(f"File should be in '{file_format}' format ")
            if os.path.isfile(output_to):
                raise ValueError(f"File {output_to} is already exists. Please chose another")
            return output_to
        else:
            target_file = self.generate_unique_file_name(dir_path=output_to, file_format=file_format)
            return target_file

    def generate_unique_file_name(self, file_format: str, dir_path: str = ""):
        """
        Generate unique file name to given directory
        :param file_format: format of file name of which we want to generate
        :param dir_path: file path
        :return: generated name with filepath
        """
        target_file = f"{dir_path}/{OUTPUT_FILE_NAME}" + "_{}." + f"{file_format}"
        counter = 1
        while os.path.isfile(target_file.format(counter)):
            counter += 1
        filename = target_file.format(counter)
        return filename

    def save_news_as_pdf(self, output_to, news_limit: int = None):
        """
        Dump loaded news into pdf file
        :param output_to:
        :param news_limit: count of news to be showen
        :return: None
        """
        util.log(msg="Start creating pdf file...", flag="INFO", show_on_console=self.show_logs)
        try:
            target_file = self.check_target_output_file(output_to, "pdf")
            page = self.get_news_page(news_limit)
            util.log(msg="Start writing data into file", flag="INFO", show_on_console=self.show_logs)
            with open(target_file, "w+b") as resultFile:
                pisa.CreatePDF(page, dest=resultFile)

            util.log(msg=f"{target_file} was created", flag="INFO", show_on_console=self.show_logs)
        except (OSError, ValueError) as err:
            util.log(msg=f"Error has occurred while converting news to html: {str(err)} ", flag="ERROR",
                     show_on_console=True)
