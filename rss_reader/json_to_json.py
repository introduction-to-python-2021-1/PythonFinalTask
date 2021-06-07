"""json_to_json module converts JSON containing html markup to JSON containing plain text.

Classes:
-------
    HtmlJsonToTextJson

Attributes:
----------
    _limit: int
    _text_json_list: list

Methods:
-------
    __init__(self, html_json_list: list, limit: int = None)
    _html_json2text_json(self, html_json_list: list, limit: int) -> list
    _html2text(html: str) -> str
    _tags2text(raw_html: str, found_links_dict: dict) -> str
    text_json_list(self) -> list
    dump_json(self) -> None
    print_json(self) -> None
"""
import sys
import json
import logging
import datetime

from bs4 import BeautifulSoup


class HtmlJsonToTextJson:
    """Class HtmlJsonToTextJson converts JSON containing html markup to JSON containing plain text. Produced plain
    text JSON could be printed directly from the class.

    Attributes:
    ----------
        _limit: int
        _text_json_list: list

    Methods:
    -------
        __init__(self, html_json_list: list, limit: int = None)
            Constructor of HtmlJsonToTextJson class instance.
        _html_json2text_json(self, html_json_list: list, limit: int) -> list
            Converts JSON values with HTML markup to plain text JSON values.
        _html2text(html: str) -> str
            Returns text without HTML markup.
        _tags2text(raw_html: str, found_links_dict: dict) -> str
            Substitutes HTML tags for links, images, and image links by plain text references.
        text_json_list(self) -> list
            Getter for self._text_json_list.
        dump_json(self) -> None
            Prints to stdout RSS feed in user readable JSON format.
        print_json(self) -> None
            Prints to stdout RSS feed in user readable JSON format as formatted plain text.
    """

    def __init__(self, html_json_list: list, limit: int = None):
        """Constructor of HtmlJsonToTextJson class instance.

        Parameters:
        ----------
        arg1: list
            html_json_list - List of dictionaries, containing RSS data in HTML format.
        arg2: int
            limit - Number of dictionaries from html_json_list to convert. By default limit=None - no limit.

        Attributes:
        ----------
        self._limit: int - Number of dictionaries from html_json_list to convert.
        self._text_json_list - List of dictionaries, containing RSS data in plain text format.


        """
        self._limit = limit
        self._text_json_list = self._html_json2text_json(html_json_list, limit)
        logging.info(f"html_json2text_json:Length of self._text_json_list = {len(self._text_json_list)}")

    def _html_json2text_json(self, html_json_list: list, limit: int) -> list:
        """_html_json2text_json - Converts JSON values with HTML markup to plain text JSON values.

        Parameters:
        ----------
        arg1: list
            text_json_list - List of dictionaries, containing RSS data in plain text format.
        arg2: int
            limit - Number of of dictionaries to convert.

        Returns:
        -------
            self.html_json_list - List of dictionaries, containing RSS data in plain html format.

        Side effects:
        ------------
        Date value (dictionary key='Date') converted from ISO format string '2021-05-31 09:00:17+03:00' to
         'Sun, 31 May 2021 09:00:17 +0300'

        Calls static methods:
            self._html2text(html) - Returns text without HTML markup
            self._tags2text(raw_html, found_links_dict) - Substitutes html tags for links, images, and image links with
                                                          their references
        """
        text_json_list = []

        logging.info("html_json2text_json:Starting")
        for entry in html_json_list[:limit]:

            if entry["Date"]:
                date = datetime.datetime.fromisoformat(entry["Date"])
                date = str(date.strftime("%a, %d %b %Y %H:%M:%S %z"))
            else:
                date = ""

            clean_json_entry = {"Feed": entry["Feed"],
                                "Title": entry["Title"],
                                "Date": date,
                                "Link": entry["Link"],
                                # substituting images links ans image links for plain text references
                                # removing all html tags
                                "Summary": self._html2text(self._tags2text(entry["Summary"], entry["Links"])),
                                "Links": entry["Links"]}

            text_json_list.append(clean_json_entry)

        return text_json_list

    @staticmethod
    def _html2text(html: str) -> str:
        """_html2text(html) static method - removes from the text html markup.
        Parameters:
        ----------
        arg1:
            html: str - Text containing HTML markup.

        Returns:
        _______
        String of plain text without HTML markup
        """
        if not html:
            return ""

        soup = BeautifulSoup(html, "lxml")
        return soup.get_text()

    @staticmethod
    def _tags2text(raw_html: str, found_links_dict: dict) -> str:

        """_tags2text(raw_html, found_links_dict) static method - Substitutes html tags for links, images, and image
        links by plain text references.

        Parameters:
        ----------
        arg1:
            raw_html: str - Text containing HTML markup
        arg2:
            found_links_dict: dictionary - Contain URL as a key and URL's sequential number as a value.

        Returns:
        ------
        String where html tags for links, images, and image links substituted with plain text references
        to found_links_dict

        Example:
        found_links_dict = {"http://www.example.com (link)" : 1,
                            "https://www.somesite.com/image.jpg (image)" : 2,
                            "some_other_link_url (link)" : 3}}

        Links:
            <a href="http://www.example.com">linkText</a> substituted as
             [link [1] linkText]
        Images:
            <img src="https://www.somesite.com/image.jpg" alt="imageDescription"> as
            [image [2] imageDescription]
        Image links:
            <a href="some_other_link_url"><img src="https://www.somesite.com/image.jpg" alt="altText"></a> as
            [link [3] image [2] altText]
        """

        if not raw_html:  # Prevents BeautifulSoup from crashing
            return ""

        soup_html = BeautifulSoup(raw_html, "lxml")

        # Pass 1 - Find image links:
        # nested tags <a href=""><img src="" alt=""></a> - (image links) will be keys of the dictionary:
        image_links_dict = dict()
        for link_src in soup_html.find_all("a"):

            alt_str = ""
            try:
                link_key = link_src['href']  # checking presence of href
            except TypeError:
                logging.info(f"tags2text:Faulty link found: {link_src}")
                continue
            try:
                img = link_src.find("img")  # checking presence of img
                image_key = img["src"]
                logging.info(f"tags2text:Nested <img> found: {link_src}")
            except TypeError:
                logging.info("tags2text:nested <img src= > not available")
                continue
            try:
                alt_str = img["alt"]  # checking presence of alt
                logging.info(f"tags2text:<img alt= > found: {alt_str}")
            except (TypeError, KeyError):
                logging.info("tags2text:<img alt= > not available")
            # Image link tags are keys, replacement text - values.
            # Replacement text formatting: [link [number] image [number] image_description]
            image_links_dict[str(link_src)] = f" [link [{found_links_dict[link_key + ' (link)']}] image " \
                                              f"[{found_links_dict[image_key + ' (image)']}] {alt_str}]"

        # Pass 2 - Find images
        image_dict = dict()
        for image_src in soup_html.find_all("img"):

            alt_str = ""
            try:
                image_key = image_src["src"]  # checking presence of src
                logging.info(f"tags2text:<img src= > found: {image_key}")
            except TypeError:
                logging.info("tags2text:<img src= > not available")
                continue
            try:
                alt_str = image_src["alt"]  # checking presence of alt
                logging.info(f"tags2text:<img alt= > found: {alt_str}")
            except (TypeError, KeyError):
                logging.info("tags2text:<img alt= > not available")
            # Image tags are keys, replacement text - values.
            # Replacement text formatting: [image [number] image_description]
            image_dict[str(image_src)] = f" [image [{found_links_dict[image_key + ' (image)']}] {alt_str}]"

        # Pass 3 - Find links
        links_dict = dict()
        for link_src in soup_html.find_all("a"):
            link_key = ""
            link_str = ""
            try:
                link_key = link_src['href']  # checking presence of href
                logging.info(f"tags2text:<a href= > found: {link_key}")
            except TypeError:
                logging.info("tags2text:<a href= > not available")
            try:
                link_str = link_src.contents[0]  # checking presence of link text
                logging.info(f"tags2text:<a > contents found: {link_str}")
            except TypeError:
                logging.info("tags2text:<a > contents not available")
            # Link tags are keys, replacement text - values.
            # Replacement text formatting: [link [number] link_description]
            links_dict[str(link_src)] = f" [link [{found_links_dict[link_key + ' (link)']}] {link_str}]"

        # HTML markup stored in soup object is different from original, loaded into soup.
        # Using here HTML corrected by soup parser. Otherwise replacement may fail due to tags mismatch in raw and
        # soup HTML.
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

    @property
    def text_json_list(self) -> list:
        """text_json_list(self) - getter for self._text_json_list

        Returns:
        ---------
            self._text_json_list - List of dictionaries, containing RSS data in plain text format.
        """
        return self._text_json_list

    def dump_json(self, limit: int = None) -> None:
        """dump_json() - Prints to stdout RSS feed in user readable JSON format.

        Parameters:
        ----------
        arg1: int
            limit - Number of dictionaries from the self._text_json_list to print. By default None - no limit.

        Returns:
        -------
            None

        Side effects:
        ------------
        Prints message when self.text_json_list is empty.

        Reads attributes:
            self._text_json_list: list - List of dictionaries, containing RSS data in plain text format.
        """
        logging.info("dump_json: Printing news in JSON format")

        if not self._text_json_list:
            print("RSS feed data not available")
            return None

        for dct in self._text_json_list[:limit]:
            json.dump(dct, sys.stdout, indent=2, ensure_ascii=False)
            print("")

        return None

    def print_json(self, limit: int = None) -> None:
        """print_json() - Prints to stdout RSS feed in user readable JSON format as formatted plain text.

        Parameters:
        arg1: int
            limit - Number of dictionaries from the self._text_json_list to print. By default None - no limit.

        Side effects:
        ------------
        Prints message when self._text_json_list is empty.

        Reads attributes:
            self._text_json_list: list - List of dictionaries, containing RSS data in plain text format.

        Dictionary keys that are always displayed: Feed, Title, Date, Link, Links
        Keys which are displayed if not empty: Summary
        """
        if not self.text_json_list:
            print("RSS feed data not available")
            return None

        logging.info("print_json: Printing news in plain text format")
        for entry in self.text_json_list[:limit]:
            print("-" * 80, flush=True)
            print(f'Feed: {entry["Feed"]}', flush=True)
            print(f'Title: {entry["Title"]}', flush=True)
            print(f'Date: {entry["Date"]}', flush=True)
            print(f'Link: {entry["Link"]}', flush=True)
            if entry["Summary"]:
                print(f'\nSummary: {entry["Summary"]}', flush=True)
            print("\nLinks:")
            for link, i in entry["Links"].items():
                print(f"[{i}] {link}")

        return None
