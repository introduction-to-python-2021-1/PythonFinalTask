import sys
import urllib.error
import xml.etree.ElementTree as ET

from urllib.request import urlopen

import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)

# function returns <class 'xml.etree.ElementTree.Element'> if URL correct.
# the networking method was intentionally created in a separate file


def get_response(url):
    try:
        xml_url = urlopen(url)
        if xml_url.status != 200:
            raise AttributeError("Bad response.")

    except AttributeError as e:
        logger.exception(e)
        sys.exit()

    except urllib.error.HTTPError as e:
        logger.exception(e)
        sys.exit()

    logger.info("Good response. Start parse.")

    return xml_url

def get_xml_tree(url):
    xml_url = get_response(url)

    try:
        xml_doc = ET.parse(xml_url)
        root = xml_doc.getroot()

        if root.tag != "rss":
            raise ValueError("This is not RSS feed")

    except ValueError as error:
        logger.error(error)
        sys.exit()

    logger.info("Parse done.")

    return root
