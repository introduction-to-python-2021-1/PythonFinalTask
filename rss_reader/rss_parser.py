import logging
import time
import datetime
import feedparser as fp
from bs4 import BeautifulSoup
import json
import sys


class RssParser:
    """
    RssParser class wraps together feedparser and BeautifulSoup module
    To work with class the following sequence required:
    1. create instance of the class: rss_feed = RssParser("https://www.yahoo.com/news/rss")
    - 2. retrieve data and parse rss feed: rss_feed.parse_url()
    3. check whether data was retrieved: rss_feed.is_empty != 0 . if empty - no data received.
    - 3. extract raw data from the feed: rss_feed.rss2raw_json()

       4. (optional)  the data will be stored in rss_feed.raw_json_list which is list of dictionaries
       To view rss_feed.raw_json_list just call: rss_feed.dump_raw_json()

    5. to remove html tags and substitute links and images with references, call: rss_feed.raw_json2clean_json()

       6. (optional) the data will be stored in rss_feed.clean_json_list which is list of dictionaries
       To view rss_feed.clean_json_list call: rss_feed.dump_raw_json()

    7. to print rss the feed, call: rss_feed.print_clean_json()
    """

    # Parsed RSS entries will be stored in the dictionary
    # json_rss = {"Feed": "", "Title": "", "Date": "", "Link": "", "Summary": "", "Content": "", "Links": {}}
    # "Links" : { 1 : "Link1", 2 : "Link2", N : "LinkN"}

    def __init__(self, url, limit=None):
        logging.info("rss_parser module activated")
        self.clean_json_list = []  # list of JSON items containing Feed, Title, Date information in plain text
        self.raw_json_list = []  # will be used to store JSON data on disc (iteration 3)
        self.url = url  # rss feed url
        self.limit = limit  # number of rss feed entries to show
        logging.info(f"Number of news to read: {self.limit}")
        self.NewsFeed = []
        self.number_of_entries = 0

        self.parse_url()
        self.rss2raw_json()
        self.raw_json2clean_json()

    def parse_url(self):
        # Loading and parsing data from target url
        try:
            self.NewsFeed = fp.parse(self.url)
            self.number_of_entries = len(self.NewsFeed.entries)  # total number of entries (news) in the rss feed
            logging.info(f"Number of news available: {self.number_of_entries}")

        # In case of error - printing detailed message and leaving NewsFeed empty
        # main function must check NewsFeed length with is_empty() method and handle the situation
        except BaseException as be:
            print(f"Error: Invalid source URL passed: {self.url}", flush=True)
            print(f"{be}", flush=True)
            self.NewsFeed = []
            self.number_of_entries = 0

    @property
    def is_empty(self):
        """ is_empty() static function - returns True if NewsFeed object is empty
            if is empty return True - main() function should stop rss feed processing
            because no data received
        """
        return not bool(self.number_of_entries)

    @staticmethod
    def html2text(html):
        """ html2text() static function - removing all html tags from input string and returning plain text """
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text()

    @staticmethod
    def append_links(links, html_snippet):
        """ receives list of [links] and string containing html markup - html_snippet
            seeking html_snippet for images and links
            links found in html_snippet argument appended to the [links] argument
            For example: <a href="www.example.com">example</a> added to the [links] as 'https://www.example.com (link)'
            """
        logging.info(f"append_links: Starting...")
        soup = BeautifulSoup(html_snippet, "lxml")

        for image_src in soup.find_all("img"):
            try:
                links.append(image_src['src'] + " (image)")
            except TypeError:
                continue
            logging.info(f"append_links:Adding image link: {image_src['src']}")

        for link_src in soup.find_all("a"):
            try:
                links.append(link_src['href'] + " (link)")
            except TypeError:
                continue
            logging.info(f"append_links:Adding reference link: {link_src['href']})")

    # @staticmethod
    # def find_links(all_links, html_snippet):  # *args
        # pass
        """ method find_links() takes as an argument HTML string and seeking for tags
            <a href=""> </a> - links
            <img src="" alt=""> - images
            extracted from tags links are added to all_links
            ['https://www.example.com (link)', 'https://www.w3schools.com/images/w3schools_green.jpg (image)',
            'https://www.w3schools.com/ (link)']
        """
    """
        soup = BeautifulSoup(html_snippet, "lxml")

        for image_src in soup.find_all("img"):
            all_links.append(image_src['src'] + " (image)")
            logging.info(f"Adding image link: {image_src['src']}")

        for link_src in soup.find_all("a"):
            all_links.append(link_src['href'] + " (link)")
            logging.info(f"Adding reference link: {link_src['href']})")
    """

    @staticmethod
    def links_list2links_dict(all_links):
        """ receives list of links. Links are just strings like "http://www.example.com (link)" or
            "https://www.somesite.com/image.jpg (image)"
            removing duplicate links while preserving list order
            returning dictionary:
             {"http://www.example.com (link)" : 1, "https://www.somesite.com/image.jpg (image)" : 2,
             "some_other_link_url (link)" : 3}
        """
        unique_links = list(dict.fromkeys(all_links))  # should preserve order and remove duplicates
        links_dict = {}  # will contain unique links and their sequential numbers
        # links_dict = {"link": sequential number i}
        for link, i in zip(unique_links, range(1, len(unique_links) + 1)):  # range() generates sequential number
            logging.info(f"[{link}] {i}")
            links_dict[link] = i
        return links_dict

    def print_raw_rss(self):
        """ print_raw_rss() prints to stdout parsed rss feed entries without formatting
        This function is used to monitor the data retrieved from different RSS feeds
        Exists for debugging purposes only
        """
        for entry in self.NewsFeed.entries[:self.limit]:
            print("-" * 80, flush=True)
            logging.info("printing raw rss feed")
            for key, val in entry.items():
                print(f"{key}: {val}", flush=True)

    def rss2raw_json(self):
        """ rss2raw_json method extracts data from feedparser module and filling in dictionary raw_json_entry
        Raw means that the data stored in the dictionary as received from the rss feed - containing html tags
        the only exclusions are Date (converted to local time), and Links (collected from Link, Summary, Content
        sections)
        """
        for entry in self.NewsFeed.entries[:]:
            logging.info("rss2raw_json:new cycle")
            raw_json_entry = {"Feed": "", "Title": "", "Date": "", "Link": "", "Summary": "", "Content": "",
                              "Links": {}, "short_date": "", "short_time": "", "url": ""}

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
                raw_json_entry["Date"] = str(published_date_local.strftime("%a, %d %b %Y %H:%M:%S %z"))
                raw_json_entry["short_date"] = str(published_date_local.strftime("%Y%m%d"))
                raw_json_entry["short_time"] = str(published_date_local.strftime("%H%M%S"))
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
            raw_json_entry["url"] = self.url

            self.raw_json_list.append(raw_json_entry)  # raw_json_entry dictionary was filled and now appended to list

    def dump_raw_json(self):
        """ dump_raw_json prints list of dictionaries contained in raw_json_list variable) """
        for dct in self.raw_json_list[:self.limit]:
            json.dump(dct, sys.stdout, indent=2)

    @staticmethod
    def tags2text(raw_html, found_links_dict):
        """
        tags2text(soup object) returns str containing html markup, where some html tags substituted with plain text
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

    def dump_clean_json(self):
        """ dump_clean_json prints list of dictionaries contained in clean_json_list variable) """
        for dct in self.clean_json_list[:self.limit]:
            json.dump(dct, sys.stdout, indent=2)

    def raw_json2clean_json(self):
        logging.info("raw_json2clean_json:new cycle")
        for entry in self.raw_json_list[:self.limit]:
            clean_json_entry = {"Feed": entry["Feed"],
                                "Title": entry["Title"],
                                "Date": entry["Date"],
                                "Link": entry["Link"],
                                # substituting images links ans image links for plain text references
                                # removing all html tags
                                "Summary": self.html2text(self.tags2text(entry["Summary"], entry["Links"])),
                                "Content": self.html2text(self.tags2text(entry["Content"], entry["Links"])),
                                "Links": entry["Links"]}

            self.clean_json_list.append(clean_json_entry)

    def print_clean_json(self):
        """ print_clean_json

        """
        for entry in self.clean_json_list[:self.limit]:
            print("-" * 80, flush=True)
            print(f'Feed: {entry["Feed"]}', flush=True)
            print(f'Title: {entry["Title"]}', flush=True)
            print(f'Date: {entry["Date"]}', flush=True)
            print(f'Link: {entry["Link"]}\n', flush=True)
            print(f'Summary: {entry["Summary"]}', flush=True)
            print(f'\nContent: {entry["Content"]}', flush=True)
            print("\nLinks:")
            for link, i in entry["Links"].items():
                print(f"[{i}] {link}")
