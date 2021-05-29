"""
    Module contains classes Parser and XmlParser
    for parsing data to dict for creating RssNews
"""
import re
import xml.etree.ElementTree as ElementTree
from sys import exit
from abc import abstractmethod, ABC
from rss_core.reader import Reader
from rss_core.rss_classes import RssItem
from utils import util

ParseError = ElementTree.ParseError

CORRECT_CHARS = {"\n": "", "\t": "", "\r": "", "&nbsp;": " ", "&#039;": "'", "&#x3C;": "<", "&#x3E;": ">",
                 "&#x26": "&", "&amp;": "&", "<![CDATA[": "", "]]>": ""}


class Parser(ABC):
    """
    Abstract class for setting parser from NewsWorker
    """

    @abstractmethod
    def parse_news(self, source, show_logs: bool = False):
        """Process data and return dict of rss news"""


class XmlParser(Parser):
    """
    Parser for NewsWorker witch received xml string from reader
    and parse it into dict fro initializing RssNews object
    """

    def __init__(self, reader: Reader = None):
        self.reader = reader

    def parse_news(self, link: str, show_logs: bool = False):
        """
        Received xml str from reader and process it into dict
        :param link: for calling reader
        :param show_logs: whether logs should be shown
        :return: dict  for creating RssNews
        """
        try:
            if not isinstance(link, str):
                raise TypeError(f"Illegal type for 'link': {str(link)}. It mast be string ")
            if len(link) == 0:
                raise ValueError("Link mast be not empty str")
            if self.reader is None:
                raise AttributeError("Reader is not initialized. Can't perform reader.get_data")
            util.log(show_on_console=show_logs, flag="INFO", msg="Start getting data from reader...")
            xml_str = self.reader.get_data(link)
            util.log(show_on_console=show_logs, flag="INFO", msg="Data was received")
            util.log(show_on_console=show_logs, flag="INFO", msg="Start converting xml to dict...")
            root = ElementTree.fromstring(xml_str)
            news_dict = self.create_rss_dict(root)
            util.log(show_on_console=show_logs, flag="INFO", msg="Dict was created successfully")
            return news_dict

        except ElementTree.ParseError as err:
            util.log(show_on_console=True,
                     flag="ERROR",
                     msg=f"Error has occurred while parsing xml (Check if parsed string is valid xml) {str(err)}")
            exit(1)
        except ConnectionError as err:
            util.log(show_on_console=True,
                     flag="ERROR",
                     msg=f"{str(err)}")
            exit(1)

    def create_rss_dict(self, xml_content: ElementTree):
        """
        Create dict from input ElementTree
        :param xml_content: ElementTree for filling rss_dict
        :return: dict with info for creating RssNews obj
        """
        news_dict = {"title": xml_content.find(".//title").text,
                     "description": xml_content.find(".//description").text or "",
                     "link": xml_content.find(".//link").text,
                     "news": []}

        news_items = xml_content.findall(".//item")
        news_dict["news"] = self.get_news_array(news_items)
        return news_dict

    def get_news_array(self, news_items):
        """
        Create array of RssItems from array of xml items with info
        :param news_items: array ox xml items
        :return: array of RssItems
        """
        news = []
        for item in news_items:
            cur_news = {elem.tag: self.strip_tag_text(elem.text) for elem in item.iter() if
                        self.strip_tag_text(elem.text) is not None or "content" in elem.tag}

            cur_news_content = []
            content_elements = {key: value for key, value in cur_news.items() if "content" in key}
            for content_element in content_elements:
                cur_news_content += [content.attrib['url'] for content in item.findall(content_element) if
                                     "url" in content.attrib]

            cur_news["content"] = cur_news_content
            news.append(RssItem(**cur_news))
        return news

    def strip_tag_text(self, tag_text: str):
        """
        Delete or replace all wrong characters from tag text
        return: performed str
        """
        if not tag_text or len(tag_text) == 0:
            return tag_text
        for wrong_chr, right_chr in CORRECT_CHARS.items():
            tag_text = tag_text.replace(wrong_chr, right_chr)
        tag_text = re.sub(r'</*\w+[^>]*?/*>', ' ', tag_text)
        return tag_text
