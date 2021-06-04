import sys
import xml.etree.ElementTree as ET

from urllib.request import urlopen

import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)

def get_response(url):
	try:
		xml_url = urlopen(url)
		if xml_url.status != 200:
			raise Exception("Bad response. Check URL address")

	except Exception as UrlError:
		logger.exception(UrlError)
		# logger.error(f"Bad URL address", exc_info= True)
		sys.exit()

	try:
		xml_doc = ET.parse(xml_url)
		root = xml_doc.getroot()

		if root.tag != "rss":
			raise Exception("This is not RSS feed")

	except Exception:
		logger.error(Exception)
		sys.exit()
	return root

def get_news(channel):
	pass