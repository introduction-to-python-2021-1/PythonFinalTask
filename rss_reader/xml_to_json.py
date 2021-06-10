"""json_to_json module converts JSON containing html markup to JSON containing plain text.

Classes:
-------
    XmlJsonConverter

Attributes:
----------
    _limit: int
    _html_json_list: list

Methods:
-------
    __init__(self, xml: str, limit: int = None)
    _xml2html_json(self, xml: str) -> list
    _append_links(links: list, html_snippet: str) -> None
    _links_list2links_dict(all_links: list) -> dict
    html_json_list(self) -> list
    dump_json(self) -> None
"""
import datetime
import logging
import sys
import json

import xml.etree.ElementTree as xmlTree
from bs4 import BeautifulSoup


class XmlJsonConverter:
    """Class XmlJsonConverter converts JSON containing html markup to JSON containing plain text.

    Attributes:
    ----------
        _limit: int
        _html_json_list: list

    Methods:
    -------
        __init__(self, xml: str, limit: int = None)
            Constructor for XmlDownloader class instance.
        _xml2html_json(self, xml: str) -> list
            Converts RSS data from XML to JSON format.
        _append_links(links: list, html_snippet: str) -> None
            Appends URLs found in html_snippet to the links argument.
        _links_list2links_dict(all_links: list) -> dict
            Returns dictionary of unique links (keys) with sequential numbers (values).
        html_json_list(self) -> list
            Getter for self._html_json_list.
        dump_json(self) -> None
            Prints list of dictionaries contained in self._html_json_list attribute.
    """
    def __init__(self, xml: str, url: str, limit: int = None):
        """Constructor for XmlDownloader class instance.

        Parameters:
        ----------
        arg1: str
            xml - XML obtained from RSS feed.
        arg2: str
            url - URL of the RSS feed.
        arg2: int
            limit - Number of JSON entries to print. Default=None - no limit.

        Attributes:
        ----------
        self._limit: int - XML obtained from URL. In case of error - empty string "".
        self._html_json_list - List of JSON entries converted from XML
        """
        self._limit = limit
        self._html_json_list = self._xml2html_json(xml, url)
        logging.info(f"xml2html_json:Length of html_json_list = {len(self.html_json_list)}")

    def _xml2html_json(self, xml: str, url: str) -> list:
        """rss2raw_json() - Converts RSS data from XML to JSON format.

        XML 'pubDate' converted to local timezone and saved to JSON in ISO format:
        XML 'pubDate' = 'Sun, 31 May 2021 09:00:17 -0400'
        JSON 'Date' = '2021-05-31 16:00:17+03:00'

        EST time 'Sun, 31 May 2021 09:00:17 EST' considered to be equal to '-0400'
        timezone 'Sun, 31 May 2021 09:00:17 -0400'

        JSON value for key 'Links' contains links collected from JSON 'Link' and 'Summary' keys values

        Format conversion:
        -----------------
        XML key -> JSON key
        'title' -> 'Feed'
        'item'/'title' -> 'Title'
        'item'/'pubDate' -> 'Date'
        'item'/'link' -> 'Link'
        'item'/'description' -> 'Summary'

        Side effects:
        ------------
        Prints to stdout error message and returns empty list in case of XML parsing error.

        Calls static methods:
            self._append_links(links: list, html_snippet: str)-Appends URLs found in html_snippet to the links argument.
            self.links_list2links_dict(all_links: list) - Returns dictionary of unique links (keys) with sequential
                                                          numbers (values).
        """
        try:
            xml_root = xmlTree.fromstring(xml)
        except Exception as e:
            print(f"RSS feed provided incompatible data\n\nError: {e}")
            return []

        try:
            feed_name = xml_root[0].find("title").text  # Feed name
            logging.info(f"xml2html_json:Feed name is {feed_name}")
        except AttributeError:
            logging.info("xml2html_json:Warning:Feed name not available")
            feed_name = ""

        html_json_list = []

        for item in xml_root[0].findall("item"):
            logging.info("xml2html_json:Parsing next item")

            html_json_entry = {"Feed": "", "Title": "", "Date": "", "Link": "", "Summary": "", "Links": {}, "URL": ""}

            found_links = []  # list of links found in <a href= /> and <img src= /> will be stored here

            html_json_entry["Feed"] = feed_name

            try:
                html_json_entry["Title"] = item.find("title").text
                logging.info(f"xml2html_json:Title found:{html_json_entry['Title']}")
            except AttributeError:
                logging.info("xml2html_json:Warning:Title not available")

            try:
                date = item.find("pubDate").text
                logging.info(f"xml2html_json:Date found:{date}")
                if date.endswith("EST"):  # eastern standard time in USA - not matches %z
                    date = date.replace("EST", "-0400")
                if date.endswith("GMT"):  # eastern standard time in USA - not matches %z
                    date = date.replace("GMT", "+0000")

                try:
                    published_date = datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
                except ValueError as e:
                    logging.info(f"_xml2html_json: Date conversion error - {e}")
                    continue

                published_date_utc = published_date.replace(tzinfo=datetime.timezone.utc)
                published_date_local = published_date_utc.astimezone()
                html_json_entry["Date"] = str(published_date_local)
            except AttributeError:
                logging.info("xml2html_json:Warning:Date not available")

            try:
                html_json_entry["Link"] = item.find("link").text
                logging.info(f"xml2html_json:Link found:{html_json_entry['Link']}")
                found_links.append(item.find("link").text + " (link)")
            except AttributeError:
                logging.info("xml2html_json:Warning:Link not available")

            try:
                html_json_entry["Summary"] = item.find("description").text
                self._append_links(found_links, item.find("description").text)
                logging.info(f"xml2html_json:Summary found")
            except AttributeError:
                logging.info("xml2html_json:Warning:Summary not available")

            html_json_entry["Links"] = self._links_list2links_dict(found_links)

            html_json_entry["URL"] = url

            html_json_list.append(html_json_entry)  # html_json_entry dictionary filled and appended to the list

        return html_json_list

    @staticmethod
    def _append_links(links: list, html_snippet: str) -> None:
        """ append_links(links, html_snippet) - Appends URLs found in html_snippet to the links argument.
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
        if not html_snippet:
            return None

        logging.info(f"append_links: Starting...")
        soup = BeautifulSoup(html_snippet, "lxml")

        for image_src in soup.find_all("img"):
            try:
                links.append(image_src['src'] + " (image)")
            except KeyError:
                continue
            logging.info(f"append_links:Added image link: {image_src['src']}")

        for link_src in soup.find_all("a"):
            try:
                links.append(link_src['href'] + " (link)")
            except KeyError:
                continue
            logging.info(f"append_links:Added reference link: {link_src['href']})")

        return None

    @staticmethod
    def _links_list2links_dict(all_links: list) -> dict:
        """links_list2links_dict(all_links: list) - Returns dictionary of unique links (keys) with sequential numbers
        (values).

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

    @property
    def html_json_list(self) -> list:
        """html_json_list() - Getter for self._html_json_list."""
        return self._html_json_list

    def dump_json(self) -> None:
        """dump_json() - Prints list of dictionaries contained in self._html_json_list attribute.

        Side effects:
        ------------
        Prints 'RSS feed data not available' when self.html_json_list == [].

        Reads attribute:
            self._html_json_list - List of dictionaries, containing RSS data in HTML format.
            self._limit - Number of dictionaries to print. By default self._limit=None - no limit.
        """
        if not self._html_json_list:
            print("RSS feed data not available")
            return None

        for dct in self.html_json_list[:self._limit]:
            json.dump(dct, sys.stdout, indent=2, ensure_ascii=False, default=str)

        return None
