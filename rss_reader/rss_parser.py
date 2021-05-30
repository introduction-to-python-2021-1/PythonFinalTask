"""RssParser module gets data from RSS feed, parsing and converting the data to a list of dictionaries used for storage
and printing. RssParser provides error handling and prints to stdout error messages in case of problems with RSS feed or
internet or connection.

Methods:
-------
    __init__(self, url: str, limit=None)
    parse_url(self) -> int
    is_empty(self) -> Boolean
    html2text(html: str) -> str
    tags2text(raw_html: str, found_links_dict: dict):
    append_links(links: list, html_snippet: str) -> None
    links_list2links_dict(all_links: str) -> dict
    rss2raw_json(self) -> None
    raw_json2clean_json(self) -> None
    dump_raw_json(self) -> None
    dump_json(self) -> None
    print_raw_rss(self) -> None
    print_json(self) -> None

Attributes:
----------
    clean_json_list: list
    raw_json_list: list
    url: str
    limit: int
    NewsFeed: list
    number_of_entries: int
"""
import sys
import logging
import time
import datetime
import json

import feedparser as fp
from bs4 import BeautifulSoup
from typing import List


class RssParser:
    """Class RssParser retrieves data from specified URL, parsing and printing RSS feed to stdout in plain text
     or JSON format.

    Parameters:
    ----------
    arg1: str
        url - RSS-feed url.
    arg2: int
        limit - limits number of RSS news printed to stdout. By default limit=None - all available news are printed.

    Attributes:
    ----------
    raw_json_list: list of dict
        Stores not processed data, received from RSS feed.

        clean_json_list contains dictionaries with structure:
        {"Feed": str, "Title": str, "Date": datetime.datetime, "Link": str, "Summary": str, "Content": str,
        "Links": dict}
            Links dictionary structure:
            "Links" : { 1 : str, 2 : str, 3 : str, ...}

    clean_json_list: list of dict
        Stores human readable text without html tags.

        clean_json_list contains dictionaries with structure:
        {"Feed": str, "Title": str, "Date": str, "Link": str, "Summary": str, "Content": str, "Links": dict}
            Links dictionary structure:
            "Links" : { 1 : str, 2 : str, 3 : str, ...}

    url: str
        Stores URL of RSS feed.
    limit: int
        Number of news form RSS feed.
    NewsFeed: list
        RSS feed data parsed by feedparser.
    number_of_entries: int
        Total number of news from RSS feed.

    Example:
    -------
    1. Create instance of the class: rss_feed = RssParser("https://www.yahoo.com/news/rss")
    2. Check whether data was retrieved:
       if rss_feed.is_empty: (no data received, stop execution) else: (step 3).
    3. Print RSS feed in plain text: rss_feed.print_json()
       or in JSON format: rss_feed.dump_json()

    Methods:
    --------
    __init__(self, url: str, limit=None)

    parse_url(self) -> int
        Returns number of news read from rss feed.
    is_empty(self) -> Boolean
        Returns True when rss feed not responding.
    html2text(html: str) -> str
        Returns string of plain text without html markup.
    append_links(links: list, html_snippet: str) -> None
        Appends URL's found in html_snippet to the links argument.
    links_list2links_dict(all_links: list) -> dict
        Returns dictionary of unique links (keys) with serial numbers (values).
    print_raw_rss(self) -> None
        Prints to stdout RSS feed data produced by feedparser module.
    rss2raw_json(self) -> None
        Converts RSS feed in feedparser format to JSON format usable for storage.
    dump_raw_json(self) -> None
        Prints to stdout RSS feed in JSON format usable for storage.
    tags2text(raw_html: str, found_links_dict: dict) -> str
        Returns string, where URL's replaced by their reference numbers from found_links_dict.
    raw_json2clean_json(self)
        Converts JSON format usable for storage to user readable JSON format.
    dump_json(self) -> None
        Prints to stdout RSS feed in user readable JSON format.
    print_json(self) -> None
        Prints to stdout RSS feed in user readable JSON format as formatted plain text.
    """

    def __init__(self, url, limit=None):
        """Constructor for RssParser class instance
        Parameters:
        ----------
        arg1: str
            url - rss-feed URL
        arg2: int
            limit - limits number of RSS news printed to stdout. By default limit=None - all available news are printed.

        Attributes:
        ----------
        self.clean_json_list = [] -
        self.raw_json_list = [] -
        self.url = url: str - contains full URL of the rss feed
        self.limit = limit: int - contains number of rss feed news to display
        self.NewsFeed = [] - parsed data from URL, provided by feedparser module
        self.number_of_entries = 0 - total number of news received from rss feed
        """
        logging.info("rss_parser module activated")
        self.clean_json_list = []  # list of JSON items containing Feed, Title, Date information in plain text
        self.raw_json_list = []  # will be used to store JSON data on disc (iteration 3)
        self.url = url  # rss feed url
        self.limit = limit  # number of rss feed entries to show
        logging.info(f"Number of news to read: {self.limit}")
        self.NewsFeed = []
        self.number_of_entries = 0

    def parse_url(self):
        """
        Method parse_url(self) retrieving RSS feed data
        Returns:
        -------
        self.number_of_entries: int - Number of news read from rss feed.

        Side effects:
        ------------
        Prints to stdout error message in case rss feed data from self.url not available.
        Reads attribute:
            self.url: str - Contains rss feed url.
        Reinitialize attributes:
            self.NewsFeed: list - RSS feed in feedparser format.
            self.number_of_entries: int - Number of entries (news) in the self.NewsFeed.
        """
        # Loading and parsing data from target url
        try:
            self.NewsFeed = fp.parse(self.url)
            self.number_of_entries = len(self.NewsFeed.entries)  # total number of entries (news) in the rss feed
            logging.info(f"Number of news available: {self.number_of_entries}")
            return self.number_of_entries
        # In case of error - printing detailed message and leaving NewsFeed empty
        # main function must check NewsFeed length with is_empty() method and handle the situation
        except BaseException as be:
            logging.info(f"parse_url:RSS feed {self.url} not responding")
            print(f"Error: Invalid source URL passed: {self.url}", flush=True)
            print(f"{be}", flush=True)
            self.NewsFeed = []
            self.number_of_entries = 0
            return self.number_of_entries

    @property
    def is_empty(self):
        """is_empty() check whether RSS feed responded
        Returns:
        _______
        True - when RSS feed did not respond. False - when RSS feed data available.

        Side effects:
        ------------
        if RSS feed available, calls:
            self.rss2raw_json() - Converts RSS feed in feedparser format to JSON format usable for storage.
            self.raw_json2clean_json() - Converts JSON format usable for storage to user readable JSON format.
        """
        if self.parse_url():
            self.rss2raw_json()
            self.raw_json2clean_json()
            return False  # Rss Feed not empty
        return True

    @staticmethod
    def html2text(html):
        """html2text(html) static function - removes from the text html markup.
        Parameters:
        ----------
        arg1:
            html: str - Text containing html markup.

        Returns:
        _______
        String of plain text without html markup
        """
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text()

    @staticmethod
    def append_links(links, html_snippet):
        """ append_links(links, html_snippet) - appends URLs found in html_snippet to the links argument
        Parameters:
        ----------
        arg1:
            links: list - List of strings. Each string contain URL and type of resource: (image) or (link)
        arg2:
            html_snippet: str - Text containing html markup

        Example:
        _______
        <a href="www.example.com">example</a>  appended as:
        'https://www.example.com (link)'
        """
        logging.info(f"append_links: Starting...")
        soup = BeautifulSoup(html_snippet, "lxml")

        for image_src in soup.find_all("img"):
            try:
                links.append(image_src['src'] + " (image)")
            except TypeError:
                continue
            logging.info(f"append_links:Added image link: {image_src['src']}")

        for link_src in soup.find_all("a"):
            try:
                links.append(link_src['href'] + " (link)")
            except TypeError:
                continue
            logging.info(f"append_links:Added reference link: {link_src['href']})")

    @staticmethod
    def links_list2links_dict(all_links):
        """links_list2links_dict(all_links) returns dictionary of unique links (keys) with sequential numbers (values).
        Parameters:
        ----------
        arg1:
            all_links: list - List of strings. Each string contain URL and type of resource: (image) or (link).
            Multiple duplicate string possible.

        Returns:
        -------
        dict[str] = int - Dictionary of unique links (keys) with sequential numbers (values).

        Example:
        _______
        all_links = [ "http://www.example.com (link)", "https://www.somesite.com/image.jpg (image)",
        "http://www.example.com (link)", "http://www.example.com (link)", "some_other_link_url (link)" ]

        return {"http://www.example.com (link)" : 1,
                "https://www.somesite.com/image.jpg (image)" : 2,
                "some_other_link_url (link)" : 3}
        """
        unique_links = list(dict.fromkeys(all_links))  # should preserve order and remove duplicates
        links_dict = {}  # will contain unique links and their sequential numbers
        # links_dict = {"link": sequential number i}

        for i, link in enumerate(unique_links, start=1):  # i - sequential number for each unique link
            logging.info(f"[{link}] {i}")
            links_dict[link] = i
        return links_dict

    def print_raw_rss(self):
        """print_raw_rss() - Prints to stdout RSS feed data produced by feedparser module.
        Side effects:
        ------------
        Number of printed news is limited by value in self.limit attribute.

        Reads attributes:
            self.NewsFeed.entries: feedparser - Contains feedparser RSS feed data
            self.limit: int - Number of news to print
        """
        for entry in self.NewsFeed.entries[:self.limit]:
            print("-" * 80, flush=True)
            logging.info("printing raw rss feed")
            for key, val in entry.items():
                print(f"{key}: {val}", flush=True)

    def rss2raw_json(self):
        """
        rss2raw_json method extracts data from feedparser module and filling in dictionary raw_json_entry
        Raw means that the data stored in the dictionary as received from the rss feed - containing html tags
        the only exclusions are Date (converted to local time), and Links (collected from Link, Summary, Content
        sections)
        """
        for entry in self.NewsFeed.entries[:]:
            logging.info("rss2raw_json:new cycle")
            raw_json_entry = {"Feed": "", "Title": "", "Date": "", "Link": "", "Summary": "", "Content": "",
                              "Links": {}}

            found_links = []  # list of links found in <a href= /> and <img src= /> will be stored here

            try:
                raw_json_entry["Feed"] = str(self.NewsFeed.feed.title)
            except AttributeError:
                logging.info("rss2raw_json:Warning:Feed name not available")

            try:
                raw_json_entry["Title"] = str(entry.title)
            except AttributeError:
                logging.info("rss2raw_json:Warning:Title not available")

            try:
                # converting time.time to datetime.datetime
                published_date = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
                published_date_utc = published_date.replace(tzinfo=datetime.timezone.utc)
                published_date_local = published_date_utc.astimezone()
                #  raw_json_entry["Date"] = str(published_date_local.strftime("%a, %d %b %Y %H:%M:%S %z"))
                #  raw_json_entry["short_date"] = str(published_date_local.strftime("%Y%m%d"))
                #  raw_json_entry["short_time"] = str(published_date_local.strftime("%H%M%S"))
                raw_json_entry["Date"] = str(published_date_local)
            except AttributeError:
                logging.info("rss2raw_json:Warning:Date not available")

            try:
                raw_json_entry["Link"] = str(entry.link)
                found_links.append(entry.link + " (link)")
            except AttributeError:
                logging.info("rss2raw_json:Warning:Link not available")

            try:
                raw_json_entry["Summary"] = str(entry.summary)
                self.append_links(found_links, raw_json_entry["Summary"]) # was find_linsk()
            except AttributeError:
                logging.info("rss2raw_json:Warning:Summary not available")

            try:
                raw_json_entry["Content"] = str(entry.content[-1]['value'])
                self.append_links(found_links, raw_json_entry["Content"])
            except AttributeError:
                logging.info("rss2raw_json:Warning:Content not available")

            raw_json_entry["Links"] = self.links_list2links_dict(found_links)
            # raw_json_entry["url"] = self.url

            self.raw_json_list.append(raw_json_entry)  # raw_json_entry dictionary was filled and now appended to list

    def dump_raw_json(self):
        """ dump_raw_json prints list of dictionaries contained in raw_json_list variable) """
        if not len(self.raw_json_list):
            print("RSS feed data not available")
            return None

        for dct in self.raw_json_list[:self.limit]:
            json.dump(dct, sys.stdout, indent=2, ensure_ascii=False, default=str)

    @staticmethod
    def tags2text(raw_html, found_links_dict):
        """tags2text(soup object) returns str containing html markup, where some html tags substituted with plain text
        Tags for:
        1. image links <a href=""><img src="" alt=""></a>
        2. images <img src="" alt="">
        3. links <a href=""> </a>
        are substituted with their short description and reference number. Reference number is taken from link_dict.
        """
        soup_html = BeautifulSoup(raw_html, "lxml")

        # Pass 1 - Find image links:
        # nested tags <a href=""><img src="" alt=""></a> - (image links) will be keys of the dictionary:
        image_links_dict = dict()
        for link_src in soup_html.find_all("a"):
            #  link_key = ""
            #  image_key = ""
            alt_str = ""
            try:
                link_key = link_src['href']
            except TypeError:
                logging.info(f"tags2text:Faulty link found: {link_src}")
                continue
            try:
                img = link_src.find("img")
                image_key = img["src"]
                logging.info(f"tags2text:Nested <img> found: {link_src}")
            except TypeError:
                logging.info("tags2text:nested <img src= > not available")
                continue
            try:
                alt_str = img["alt"]
                logging.info(f"tags2text:<img alt= > found: {alt_str}")
            except (TypeError, KeyError):
                logging.info("tags2text:<img alt= > not available")
            # Image link tags are keys, replacement text - values.
            # Replacement text formatting: [link [number] image [number] image_description]
            image_links_dict[str(link_src)] = f"[link [{found_links_dict[link_key + ' (link)']}] image " \
                                              f"[{found_links_dict[image_key + ' (image)']}] {alt_str}] "

        # Pass 2 - Find images
        image_dict = dict()
        for image_src in soup_html.find_all("img"):
            #  image_key = ""
            alt_str = ""
            try:
                image_key = image_src["src"]
                logging.info(f"tags2text:<img src= > found: {image_key}")
            except TypeError:
                logging.info("tags2text:<img src= > not available")
                continue
            try:
                alt_str = image_src["alt"]
                logging.info(f"tags2text:<img alt= > found: {alt_str}")
            except (TypeError, KeyError):
                logging.info("tags2text:<img alt= > not available")
                # continue
            # Image tags are keys, replacement text - values.
            # Replacement text formatting: [image [number] image_description]
            image_dict[str(image_src)] = f"[image [{found_links_dict[image_key + ' (image)']}] {alt_str}] "

        # Pass 3 - Find links
        links_dict = dict()
        for link_src in soup_html.find_all("a"):
            link_key = ""
            link_str = ""
            try:
                link_key = link_src['href']
                logging.info(f"tags2text:<a href= > found: {link_key}")
            except TypeError:
                logging.info("tags2text:<a href= > not available")
            try:
                link_str = link_src.contents[0]
                logging.info(f"tags2text:<a > contents found: {link_str}")
            except TypeError:
                logging.info("tags2text:<a > contents not available")
            # Link tags are keys, replacement text - values.
            # Replacement text formatting: [link [number] link_description]
            links_dict[str(link_src)] = f"[link [{found_links_dict[link_key + ' (link)']}] {link_str}] "

        # html markup stored in soup object is different from original, loaded into soup
        # using here html corrected by soup parser. Otherwise replacement may fail due to tags mismatch in raw and
        # soup html
        modified_html = str(soup_html)

        # Modification 1 - Replacing image links tags with plain text
        for image_link, replacement_text in image_links_dict.items():
            logging.info(f"tags2text:Replacing {image_link} with {replacement_text}")
            modified_html = modified_html.replace(image_link, replacement_text)

        # Modification 2 - Replacing image tags with plain text
        for image_src, replacement_text in image_dict.items():
            logging.info(f"tags2text:Replacing {image_src} with {replacement_text}")
            modified_html = modified_html.replace(image_src, replacement_text)

        # Modification 3 - Replacing link tags with plain text
        for links_src, replacement_text in links_dict.items():
            logging.info(f"tags2text:Replacing {links_src} with {replacement_text}")
            modified_html = modified_html.replace(links_src, replacement_text)

        return modified_html

    def raw_json2clean_json(self):
        logging.info("raw_json2clean_json:new cycle")
        for entry in self.raw_json_list[:self.limit]:
            date = datetime.datetime.fromisoformat(entry["Date"])
            clean_json_entry = {"Feed": entry["Feed"],
                                "Title": entry["Title"],
                                "Date": str(date.strftime("%a, %d %b %Y %H:%M:%S %z")),
                                "Link": entry["Link"],
                                # substituting images links ans image links for plain text references
                                # removing all html tags
                                "Summary": self.html2text(self.tags2text(entry["Summary"], entry["Links"])),
                                "Content": self.html2text(self.tags2text(entry["Content"], entry["Links"])),
                                "Links": entry["Links"]}

            self.clean_json_list.append(clean_json_entry)

    def dump_json(self):
        """dump_json() - Prints to stdout RSS feed in user readable JSON format.

        Side effects:
        ------------
        Number of printed news is limited by value in self.limit attribute.

        Reads attributes:
            self.clean_json_list: list - List of dictionaries, containing RSS data in plain text format.
            self.limit: int - Number of news to print
        """
        logging.info("dump_json: Printing news in JSON format")

        if not len(self.clean_json_list):
            print("RSS feed data not available")
            return None

        for dct in self.clean_json_list[:self.limit]:
            json.dump(dct, sys.stdout, indent=2, ensure_ascii=False)
            print("")

    def print_json(self):
        """print_json() - Prints to stdout RSS feed in user readable JSON format as formatted plain text.

        Side effects:
        ------------
        Number of printed news is limited by value in self.limit attribute.

        Reads attributes:
            self.clean_json_list: list - List of dictionaries, containing RSS data in plain text format.
            self.limit: int - Number of news to print

        Dictionary keys that are always displayed: Feed, Title, Date, Link, Links
        Keys which are displayed if not empty: Summary, Content
        """
        if not self.clean_json_list:
            print("RSS feed data not available")
            return None

        logging.info("print_json: Printing news in plain text format")
        for entry in self.clean_json_list[:self.limit]:
            print("-" * 80, flush=True)
            print(f'Feed: {entry["Feed"]}', flush=True)
            print(f'Title: {entry["Title"]}', flush=True)
            print(f'Date: {entry["Date"]}', flush=True)
            print(f'Link: {entry["Link"]}', flush=True)
            if entry["Summary"]:
                print(f'\nSummary: {entry["Summary"]}', flush=True)
            if entry["Content"]:
                print(f'\nContent: {entry["Content"]}', flush=True)
            print("\nLinks:")
            for link, i in entry["Links"].items():
                print(f"[{i}] {link}")
