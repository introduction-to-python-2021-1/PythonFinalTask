import sys
from itertools import islice
import json

from urllib.request import urlopen
import xml.etree.ElementTree as ET

import app_logger

logger = app_logger.get_logger(__name__)


# This class parses the site, handles data
# Outputs to stdout or file like .log or .json
class feed_container:
	def __init__(self, url, args):

		logger.info(f"Class {self.__class__.__name__}: initialization start.")
		self.url = url

		self.__get_response()
		self.__get_feed_info()

		logger.info(f"Class {self.__class__.__name__}: initialization done.")

	def __get_response(self):
		try:
			self.xml_url = urlopen(self.url)
			if self.xml_url.status != 200:
				raise Exception("Bad response. Check URL address")

		except Exception:
			logger.exception(Exception)
			# logger.error(f"Bad URL address", exc_info= True)
			sys.exit()

		try:
			self.xml_doc = ET.parse(self.xml_url)
			self.root = self.xml_doc.getroot()

			if self.root.tag != "rss":
				raise Exception("This is not RSS feed")

		except Exception:
			logger.error(Exception)
			sys.exit()

	def __get_feed_info(self):
		logger.info(f"Class {self.__class__.__name__}: get all channel date.")
		self.__get_feed_title()
		self.__get_feed_description()
		self.__get_feed_link()
		self.__get_feed_date()
		self.__get_feed_copyright()
		self.__get_items()
		logger.info(f"Class {self.__class__.__name__}: data collection is done.")

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
			  f"\nChannel date: {self.feed_date}"
			  f"\nChannel copyright: {self.feed_copyright}")

	def print_news(self, limit):

		size = limit

		for item in islice(self.channel_items, 0, size):
			print("\n")
			for key, value in item.items():
				print(f"{key}: {value}")

	# this method return news
	def get_news(self, limit):
		size = limit
		news = []

		for item in islice(self.channel_items, 0, size):
			news.append(item)

		return news

	# this method saves news in json format
	def save_as_json(self, limit):
		size = limit
		news = []

		for item in islice(self.channel_items, 0, size):
			news.append(item)
			with open("news.json", "w") as file:
				json.dump(news, file, indent=4)
