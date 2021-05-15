import feedparser as fp
import re
import logging


"""
number_of_entries = len(NewsFeed.entries)
print(f"Number of news read: {number_of_entries}")

entry = {}

for index in range(number_of_entries):
    entry = NewsFeed.entries[index]
    print(f"{index + 1}: {entry.title}")

print(entry.keys())
"""

class RssParser:
    """Wrap class for feedparser module"""

    def __init__(self, url, limit=None):
        logging.info("rss_parser module activated")
        self.url = url
        self.limit = limit
        self.entry = {}

        # try:
        self.NewsFeed = fp.parse(url)
        self.number_of_entries = len(self.NewsFeed.entries)
        print(f"Number of entires: {self.number_of_entries}")
        # except BaseException as be:
        # print(f"Error: Invalid source URL passed: {self.url}")
        # print(f"{be}")
        # exit(1)

    def not_empty(self):
        if self.number_of_entries:
            return True
        else:
            return False

    def print_raw_rss_feed(self):
        self.number_of_entries = len(self.NewsFeed.entries)

        if self.number_of_entries == 0:
            print("No entries found", flush=True)
            return None

        print(f"Number of news read: {self.number_of_entries}", flush=True)

        for index in range(self.number_of_entries):
            self.entry = self.NewsFeed.entries[index]
            print(f"{index + 1}: {self.entry.title}", flush=True)

        print(self.entry.keys())

    # using feedparser module to connect to RSS feed URL, receive and parse data
    def get_rss_limited_feed(self):

        if (self.limit is None) | (self.limit > self.number_of_entries):
            logging.info(f"Output unlimited")
            return self.NewsFeed.entries[:]
        else:
            logging.info(f"Output limited to {self.limit}")
            return self.NewsFeed.entries[:self.limit]

    # returns plain text RSS feed
    def text_rss(self):

        return None

    # returns RSS feed in HTML format
    def html_rss(self):

        return None

    def print_raw_rss(self):
        for self.entry in self.get_rss_limited_feed():
            print("-" * 80)
            for key, val in self.entry.items():
                print(f"{key}: {val}")


