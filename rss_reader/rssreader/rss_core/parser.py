"""
    Module contains classes Parser and XML2RSSDict
    for parsing data to dict for creating RSSNews
"""
import re
import xml.etree.ElementTree as ElementTree
from abc import abstractmethod, ABC
from rssreader.rss_core.reader import Reader
from rssreader.rss_core.rss_classes import RSSItem
from rssreader.utils import util

ParseError = ElementTree.ParseError

_correct_chrs = {"\n": "", "\t": "", "\r": "", "&nbsp;": " ", "&#039;": "'", "&#x3C;": "<", "&#x3E;": ">",
                 "&#x26": "&", "&amp;": "&", "<![CDATA[": "", "]]>": ""}


class Parser(ABC):
    """

    Abstract class for setting parser from NewsWorker
    """

    @abstractmethod
    def parse_news(self, source, news_limit: int = None, show_logs: bool = False):
        """Process data and return dict of rss news"""


class XMLParser(Parser):
    """

    Parser for NewsWorker witch received xml string from reader
    and parse it into dict fro initializing RssNews object
    """

    def __init__(self, reader: Reader = None):
        self.reader = reader

    def parse_news(self, link: str, news_limit: int = None, show_logs: bool = False):
        """

        Received xml str from reader and process it into dict
        :param link: for calling reader
        :param news_limit: count of news for return
        :param show_logs: whether logs should be shown
        :return: dict  for creating RSSNews
        """
        try:
            if not isinstance(link, str):
                raise TypeError(f"(XMLParser.parse_news) Illegal type for 'link': {str(link)}. It mast be string ")
            if len(link) == 0:
                print("I AM HERE!")
                raise ValueError("Link mast be not empty str")
            print("CONTINUE")
            if news_limit is not None:
                if not isinstance(news_limit, int):
                    raise TypeError("(XMLParser.parse_news) Illegal type for 'news_limit'. It mast be int or None ")
                if news_limit < 0:
                    raise ValueError(
                        "(XMLParser.parse_news) Illegal value for 'news_limit'. It mast be int >=0 or None")
            if self.reader is None:
                raise AttributeError("(XMLParser.parse_news) Reader is not initialized. Can't perform reader.get_data")
            util.log(show_on_console=show_logs, flag="INFO", msg="Start getting data from reader...")
            xml_str = self.reader.get_data(link)
            util.log(show_on_console=show_logs, flag="INFO", msg="Data was received")
            util.log(show_on_console=show_logs, flag="INFO", msg="Start converting xml to dict...")
            root = ElementTree.fromstring(xml_str)
            news_dict = self.create_rss_dict(root, news_limit)
            util.log(show_on_console=show_logs, flag="INFO", msg="Dict was created successfully")
            return news_dict
        except ParseError as err:
            print(type(err))
            util.log(show_on_console=True,
                     flag="ERROR",
                     msg=f"{err.__class__} at XMLParser.parse_news: {str(err)}\n(Check if parsed str is valid xml)")
            return {}

    def create_rss_dict(self, xml_content: ElementTree, news_limit: int = None):
        """

        Create dict from input ElementTree
        :param xml_content: ElementTree for filling rss_dict
        :param news_limit: count of news to be got
        :return: dict with info for creating RSSNews obj
        """
        news_dict = {"title": xml_content.find(".//title").text,
                     "description": xml_content.find(".//description").text,
                     "link": xml_content.find(".//link").text,
                     "news": []}
        news_items = xml_content.findall(".//item")
        news_count = len(news_items) if news_limit is None else min(len(news_items), news_limit)
        news_dict["news"] = self.get_news_array(news_items, news_count)
        return news_dict

    def get_news_array(self, news_items, news_count):
        """

        Create array of RSSItems from array of xml items with info
        :param news_items: array ox xml items
        :param news_count: count of news
        :return: array of RSSItems
        """
        news = []
        for i in range(0, news_count):
            item = news_items[i]
            cur_news = {elem.tag: self.strip_tag_text(elem.text) for elem in item.iter()}
            content_ok = []
            for element in cur_news.keys():
                if "content" in element:
                    for content in item.findall(element):
                        content_ok += [content.attrib['url']]
            cur_news["content"] = content_ok
            news.append(RSSItem(**cur_news))
        return news

    def strip_tag_text(self, tag_text: str):
        """

        Delete or replace all wrong characters from tag text
        return: performed str
        """
        if not tag_text or len(tag_text) == 0:
            return tag_text
        for wrong_chr, right_chr in _correct_chrs.items():
            tag_text = tag_text.replace(wrong_chr, right_chr)
        tag_text = re.sub(r'<\w+[^>]+?/>', '', tag_text)
        return tag_text
