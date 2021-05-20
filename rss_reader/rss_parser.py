# import re
# import html2text
import logging
import time
import datetime
# from html.parser import HTMLParser
import feedparser as fp
from bs4 import BeautifulSoup


"""
class HTMLFilter(HTMLParser):
    text = ""

    def error(self, message):
        print(f"Error: HTMLParser - {message}")

    def handle_data(self, data):
        self.text += data
"""

class RssParser:
    """Class wraps together feedparser and BeautifulSoup module"""

    # Parsed RSS entries will be stored in the dictionary
    json_RSS = {"Feed": "", "Title": "", "Date": "", "Link": "", "Summary": "", "Content": "", "Links": {}}
    # "Links" : { 1 : "Link1", 2 : "Link2", N : "LinkN"}

    def __init__(self, url, limit=None):
        logging.info("rss_parser module activated")
        json_list = dict()

        self.url = url
        self.limit = limit
        logging.info(f"Number of news to read: {self.limit}")

        # Let's try to load and parse data from target url
        try:
            self.NewsFeed = fp.parse(url)
            self.number_of_entries = len(self.NewsFeed.entries)
            logging.info(f"Number of news available: {self.number_of_entries}")

        # In case of error - printing detailed message and leaving NewsFeed empty
        # main function must check NewsFeed length with not_empty() method and handle the situation
        except BaseException as be:
            print(f"Error: Invalid source URL passed: {self.url}", flush=True)
            print(f"{be}", flush=True)
            self.NewsFeed = []
            self.number_of_entries = 0

    @property
    def is_empty(self):
        """ is_empty() static function - returns True if NewsFeed object is empty """
        return not bool(self.number_of_entries)

    @staticmethod
    def html2text(html):
        """ html2text() static function - removing html tags from input string and returning plain text """
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text()

    @staticmethod
    def append_links(links, html_snippet):
        soup = BeautifulSoup(html_snippet, "lxml")

        for image_src in soup.find_all("img"):
            links.append(image_src['src'] + " (image)")
            logging.info(f"Adding image link: {image_src['src']}")

        for link_src in soup.find_all("a"):
            links.append(link_src['href'] + " (link)")
            logging.info(f"Adding reference link: {link_src['href']})")

    def print_raw_rss(self):
        """ print_raw_rss() prints to stdout parsed rss feed entries without formatting
        This function is used monitor data retrieved from different RSS feeds
        """

        # for entry in self.get_rss_limited_feed():
        for entry in self.NewsFeed.entries[:self.limit]:
            print("-" * 80, flush=True)
            logging.info("printing raw rss feed")
            for key, val in entry.items():
                print(f"{key}: {val}", flush=True)

    def print_rss(self):

        for entry in self.NewsFeed.entries[:self.limit]:

            found_links = []  # list of links <a href= /> and <img src= /> will be stored here
            print("-" * 80)

            try:
                print(f"Feed: {self.NewsFeed.feed.title}\n", flush=True)
            except AttributeError:
                logging.info("Warning:Feed name not available")

            try:
                print(f"Title: {entry.title}", flush=True)
            except AttributeError:
                logging.info("Warning:Title not available")

            try:
                # converting time.time to datetime.datetime
                published_date = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
                published_date_utc = published_date.replace(tzinfo=datetime.timezone.utc)
                published_date_local = published_date_utc.astimezone()
                print(f"Date: {published_date_local.strftime('%a, %d %b %Y %H:%M:%S %z')}", flush=True)
            except AttributeError:
                logging.info("Warning:Date not available")

            try:
                print(f"Link: {entry.link}\n", flush=True)
                found_links.append(entry.link + " (link)")
            except AttributeError:
                logging.info("Warning:Link not available")

            try:
                pass
                # found_links.append(entry.media_content[0]['url'])
                # print(f"{entry.media_content[0]['url']}")
            except AttributeError:
                logging.info("Warning:Media not available")

            try:
                # f = HTMLFilter()
                # f.feed(entry.summary)
                # print(f"Summary: {f.text}")
                print(f"Summary: {self.html2text(entry.summary)}")
                self.append_links(found_links, entry.summary)
            except AttributeError:
                logging.info("Warning:Summary not available")

            try:
                # f1 = HTMLFilter()
                # f1.feed(entry.content[-1]['value'])
                # print(f"\nContent: \n{f1.text.strip()}")

                print(f"\nContent: {self.html2text(entry.content[-1]['value'])}")

                self.append_links(found_links, entry.content[-1]['value'])
            except AttributeError:
                logging.info("Warning:Content not available")

            try:
                # print(f"Author: {entry.author}")
                pass
            except AttributeError:
                logging.info("Warning:Author not available")

            print("\nLinks:")
            found_links = set(found_links)  # removing duplicate links by casting list to set
            for i, link in zip(range(1, len(found_links) + 1),
                               found_links):  # range is used as link index while printing
                print(f"[{i}] {link}")

        """
        print(self.NewsFeed)
        
        print(f"Feed title:{self.NewsFeed.feed.title}", flush=True)
        print(f"Feed link:{self.NewsFeed.feed.link}", flush=True)
        print(f"Feed description:{self.NewsFeed.feed.description}", flush=True)
        print(f"Feed published parsed:{self.NewsFeed.feed.published_parsed}")
        """
