import sys
from itertools import islice

from urllib.request import urlopen
import xml.etree.ElementTree as ET
import app_logger

logger = app_logger.get_logger(__name__)

class feed_Container:
  def __init__(self, url):
    try:
      self.xml_url = urlopen(url)
      if self.xml_url.status != 200:
        raise Exception("Bad response")

    except Exception:
      sys.exit()

    self.xml_doc = ET.parse(self.xml_url)
    self.root = self.xml_doc.getroot()

    self.__get_feed_info()


  def __get_feed_title(self):
    self.feed_title = self.root.findtext("channel/title")

  def __get_feed_date(self):
    self.feed_date = self.root.findtext("channel/pubDate")

  def __get_feed_link(self):
    self.feed_link = self.root.findtext("channel/link")

  def __get_feed_description(self):
    self.feed_description = self.root.findtext("channel/description")

  def __get_feed_info(self):
    self.__get_feed_title()
    self.__get_feed_description()
    self.__get_feed_link()
    self.__get_feed_date()
    self.__get_items()

  def __get_items(self):
    self.channel_items = []
    for i, item in enumerate(self.root.iterfind("channel/item")):

      self.channel_items.append({
        "Title": item.findtext("title"),
        "Date": item.findtext("pubDate"),
        "Link": item.findtext("link"),
      })

  def print_feed_Info(self):
    print(f"\nChannel title: {self.feed_title}",
          f"\nChannel link: {self.feed_link}"
          f"\nChannel description: {self.feed_description}"
          f"\nChannel date: {self.feed_date}")

  def print_items(self, limit):
    self.limit = limit

    for item in islice(self.channel_items, 0, self.limit):
      print("\n")
      for key, value in item.items():
        print(f"{key}: {value}")