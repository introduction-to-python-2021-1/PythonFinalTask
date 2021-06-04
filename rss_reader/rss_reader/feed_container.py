from itertools import islice
import json

import rss_reader.channel_Parser as channel_Parser
import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)


# This class parses the site, handles data
# Outputs to stdout or file like .log or .json
class FeedContainer:
	def __init__(self, url):

		logger.info(f"Class {self.__class__.__name__}: initialization start.")

		self.root = channel_Parser.get_response(url)
		self.__get_feed_info()

		logger.info(f"Class {self.__class__.__name__}: initialization done.")

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
		for item in islice(self.channel_items, 0, limit):
			print("\n")
			for key, value in item.items():
				print(f"{key}: {value}")

	# this method return news
	def get_news(self, limit):
		return self.channel_items[limit]

	# this method saves news in json format
	def save_as_json(self, limit):
		news = self.channel_items[:limit]
		with open("news.json", "w") as file:
			file.write(json.dumps(news, indent = 4))
