from itertools import islice
import json
from datetime import datetime
from json2html import json2html
from xhtml2pdf import pisa

import rss_reader.channel_parse as channel_parser
import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)


# This class parses the site, handles data
# Outputs to stdout or file like .log or .json
class FeedContainer:
    # in __init__ class get 'xml.etree.ElementTree.Element'>
    # for dividing the soup into ingredients
    def __init__(self, url):

        logger.info(f"Class {self.__class__.__name__}: initialization start.")

        self.root = channel_parser.get_xml_tree(url)
        self.__channel_items = []
        self.__get_feed_info()

        logger.info(f"Class {self.__class__.__name__}: initialization done.")

    # this method get channel info and items.
    # All methods are divided into blocks for possible rewriting.
    def __get_feed_info(self):
        logger.info(f"Class {self.__class__.__name__}: get all channel date.")
        self.__get_feed_title()
        self.__get_feed_description()
        self.__get_feed_link()
        self.__get_feed_date()
        self.__get_feed_copyright()
        self.__get_items()
        logger.info(
            f"Class {self.__class__.__name__}: data collection is done.")

    def __get_feed_title(self):
        self.feed_title = self.root.findtext("channel/title")

    def __get_feed_date(self):
        self.feed_date = self.root.findtext("channel/pubDate")

    def __get_feed_link(self):
        self.feed_link = self.root.findtext("channel/link")

    def __get_feed_description(self):
        self.feed_description = self.root.findtext("channel/description")

    def __get_feed_copyright(self):
        self.feed_copyright = self.root.findtext("channel/copyright")

    def __get_items(self):
        for i, item in enumerate(self.root.iterfind("channel/item")):
            self.__channel_items.append({
                "Title": item.findtext("title"),
                "Date": item.findtext("pubDate"),
                "Link": item.findtext("link"),
            })

    # print feed info in stdout
    # not support --json
    def print_feed_Info(self):
        print(f"\nChannel title: {self.feed_title}",
              f"\nChannel link: {self.feed_link}"
              f"\nChannel description: {self.feed_description}"
              f"\nChannel date: {self.feed_date}"
              f"\nChannel copyright: {self.feed_copyright}")

    # class<feed_container> get all news from the feed in __init__
    # this method just print news within a certain limit
    def print_news(self, limit=50):
        count = 1
        for item in islice(self.__channel_items, 0, limit):
            print(f"\n {count}")
            count += 1
            for key, value in item.items():
                print(f"{key}: {value}")

    # class<feed_container> get all news from the feed in __init__
    # his method just print news within a certain limit in json format
    def print_news_json_format(self, limit=50):
        json_formatted_list = json.dumps(self.__channel_items[:limit], indent=4, ensure_ascii=False)
        print(json_formatted_list)

    # class<feed_container> get all news from the feed in __init_
    # this method just print news by date within a certain limit
    def print_news_by_date(self, date, limit=50):
        news_by_date = self.get_news_by_date(date, limit)
        count = 1

        for item in islice(news_by_date, 0, limit):
            print(f"\n {count}")
            count += 1
            for key, value in item.items():
                print(f"{key}: {value}")

    # class<feed_container> get all news from the feed in __init_
    # this method just print news by date within a certain limit in json format
    def print_news_by_date_json_format(self, date, limit):
        news_by_date = self.get_news_by_date(date, limit)
        json_formatted_list = json.dumps(news_by_date, indent=4, ensure_ascii=False)
        print(json_formatted_list)

    # class<feed_container> get all news from the feed in __init__
    # this method returns news within a certain limit
    def get_news(self, limit=50):
        return self.__channel_items[:limit]

    def get_news_to_save(self, limit=50):
        news_to_save = []

        for i, item in enumerate(self.root.iterfind("channel/item")):
            news_to_save.append({
                "Channel": self.feed_title,
                "Title": item.findtext("title"),
                "Date": item.findtext("pubDate"),
                "Link": item.findtext("link"),
            })
        return news_to_save[:limit]

    # class<feed_container> get all news from the feed in __init__
    # this method return news by date and limit if need

    def get_news_by_date(self, date, limit=50):
        news_by_date = []

        for i, item in enumerate(self.root.iterfind("channel/item")):
            item_date = datetime.strptime(item.findtext("pubDate"), "%Y-%m-%dT%H:%M:%SZ")
            item_date = item_date.replace(hour=0, minute=0, second=0)

            if item_date == datetime.strptime(date, "%Y%m%d"):
                news_by_date.append({
                    "Title": item.findtext("title"),
                    "Date": item.findtext("pubDate"),
                    "Link": item.findtext("link"),
                })
        return news_by_date[:limit]

    # this method saves news in json format
    def save_as_json(self, limit=50):
        with open("../tmp/news.json", 'a', encoding="utf-8") as file:
            file.write(json.dumps(self.get_news_to_save(limit), indent=4, ensure_ascii=False))

    # unused
    def save_as_json_by_date(self, date, limit=50):
        with open("../tmp/news.json", 'w', encoding="utf-8") as file:
            file.write(json.dumps(self.get_news_by_date(date, limit), indent=4, ensure_ascii=False))

    def news_2_html(self, limit=50):
        json_news = json.dumps(self.get_news(limit))
        with open("../tmp/news.html", 'w', encoding="utf-8") as file:
            file.write(json2html.convert(json=json_news))

    def news_2_pdf(self, limit=50):
        json_news = json.dumps(self.get_news(limit))
        html_news = json2html.convert(json=json_news)
        with open("../tmp/news.pdf", 'w+b', encoding="utf-8") as file:
            pisa.CreatePDF(html_news, file)

    def print_news_by_args(self, date, limit=50,  json=False):
        if json and date:
            self.print_news_by_date_json_format(date, limit)
        elif json:
            self.print_news_json_format(limit)
        else:
            if date:
                self.print_news_by_date(date, limit)
            else:
                self.print_news(limit)
