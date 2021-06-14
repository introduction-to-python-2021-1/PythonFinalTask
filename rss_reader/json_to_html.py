"""json_to_html module converts JSON to HTML file.

Classes:
-------
    HtmlJsonToHtml

Attributes:
----------
    _image_directory_path: str
    _limit: int

Methods:
-------
    __init__(self, limit=None, base_dir="", date="")
    change_img_url(raw_html, new_url) -> [str]
    raw_rss2html_file(self, html_file_name, raw_rss_list) -> None
"""
import datetime
import logging
import os
import re

from bs4 import BeautifulSoup


class HtmlJsonToHtml:
    """Class HtmlJsonToHtml converts JSON to HTML file.

    Attributes:
    ----------
        _image_directory_path: str
        _limit: int

    Methods:
    -------
        __init__(self, limit=None, base_dir="", date="")
            Constructor of HtmlJsonToTextJson class instance.
        change_img_url(raw_html, new_url) -> [str]
            Replace image URLs in the html markup with new URLs. Image file name not changing while replacement.
        raw_rss2html_file(self, html_file_name, raw_rss_list) -> None
            Converts list of dictionaries to string with HTML markup and saves produced string to a file.
    """
    def __init__(self, base_dir=".rss_reader", limit=None):
        """Constructor of HtmlJsonToTextJson class instance.

                Parameters:
                ----------
                arg1: str
                    base_dir - JSON storage directory.
                arg2: str
                    date - Date of RSS publication.
                arg3: int
                    limit - Number of JSON dictionaries to load.

                Attributes:
                -----------
                self._image_directory_path -  Directory path including JSON storage directory and date directory.
                self._limit - Number of JSON dictionaries to load.
        """

        self._image_directory_path = os.path.join(os.path.expanduser("~"), base_dir, "")
        self._limit = limit

    @staticmethod
    def change_img_url(raw_html: str, new_url: str) -> str:
        """change_img_url() - Replace image URLs in the html markup with new URLs. Image file name
        not changing while replacement.

        Parameters:
        ----------
        arg1: srt
            raw_html - String containing HTML markup.
        arg2: int
            new_url - String with new path.

        Returns:
        _______
            modified_html - String containing HTML markup with replaced image link URLs.
        """
        if not raw_html:  # Protect BeautifulSoup from crashing.
            return ""

        soup_html = BeautifulSoup(raw_html, "lxml")
        modified_html = str(soup_html)
        image_dict = dict()

        if new_url == "":  # changing the url if provided url not None
            return modified_html

        for image_src in soup_html.find_all("img"):
            image_url = ""
            try:
                image_url = image_src["src"]
                logging.info(f"change_img_url:<img src= > found: {image_url}")
            except TypeError:
                logging.info("change_img_url:<img src= > not available")
                continue
            # image urls are keys, replacement text is new url + filename.
            # Replacement text formatting: url\filename.ext
            if re.match(r".*\.(gif|jpe?g|bmp|png|apng|avif|svg|webp|ico|cur|tif|tiff)", image_url):
                # the last element of url is filename.ext
                image_dict[str(image_url)] = os.path.join(new_url, str(image_url).split("/")[-1])

        for image_url, changed_image_url in image_dict.items():
            logging.info(f"change_img_url:Replacing {image_url} with {changed_image_url}")
            modified_html = modified_html.replace(image_url, changed_image_url)

        return modified_html

    def raw_rss2html_file(self, html_file_name: str, raw_rss_list, replace_links: bool) -> None:
        """raw_rss2html_file() - Converts list of dictionaries to string with HTML markup and saves produced string
        to a file. Optionally replaces image links with links to RSS storage.

        Parameters:
        ----------
        arg1: str
            html_file_name - File name to save HTML markup.
        arg2: int
            raw_rss_list - List of dictionaries containing RSS data.
        arg3: bool
            replace_links - Replaces image links with links to RSS storage if True.

        Returns:
        _______
            None

        Side effects:
        ------------
        Calls static method:
            change_img_url(raw_html, new_url) - Replace image URLs in the html markup with new URLs. Image file name
            not changing while replacement.
        """
        try:
            with open(html_file_name, "w+", encoding="utf-8") as html_outfile:
                logging.info(f"Saving html file: {html_file_name}")
                html_outfile.write("<!DOCTYPE html>\n<html>\n")
                html_outfile.write(f"<head>\n<meta charset=\"utf-8\"/>\n<title>{raw_rss_list[0]['Feed']}</title>\n<"
                                   "/head>\n<body>")

                for entry in raw_rss_list[:self._limit]:
                    html_outfile.write(f"\n<p>{entry['Feed']}</p>\n")

                    html_outfile.write(f"\n<h2>{entry['Title']}</h2>\n")

                    try:  # In case of data conversion error - most likely entry[Date"] is empty.
                        date = datetime.datetime.fromisoformat(entry["Date"])
                    except ValueError:
                        date = ""

                    if date:  # In case date string not empty - converting it and printing formatted date.
                        html_outfile.write(f"\n<p><b>Date:</b> {date.strftime('%a, %d %b %Y %H:%M:%S %z')}</p>\n")
                    else:  # Otherwise printing empty date
                        html_outfile.write(f"\n<p><b>Date:</b></p>\n")

                    html_outfile.write(f"\n<p><b>Link:</b> {entry['Link']}</p>\n")

                    if entry["Summary"]:
                        if replace_links:

                            url_dir = "".join([char for char in entry["URL"].lower() if (97 <= ord(char) <= 122)])
                            date_dir = date.strftime("%Y%m%d")
                            saved_image_location = os.path.join(self._image_directory_path, url_dir, date_dir)

                            logging.info(f"raw_rss2html_file:Replacing image links with new path "
                                         f"{saved_image_location}")

                            html_outfile.write("\n<h4>Summary:</h4>\n")
                            html_outfile.write(f"\n<p>{self.change_img_url(entry['Summary'], saved_image_location)}"
                                               f"</p>\n")
                        else:
                            html_outfile.write("\n<h4>Summary:</h4>\n")
                            html_outfile.write(f"\n<p>{entry['Summary']}</p>\n")

                    html_outfile.write("\n<h4>Links:</h4>\n")
                    for link, number in entry["Links"].items():
                        url, description = link.split()
                        html_outfile.write(f'\n<p>[{number}] <a href ="{url}">{url}</a> {description}</p>\n')

                    html_outfile.write("\n<hr></hr>\n")

                html_outfile.write("\n</body>\n</html>\n")

        except FileNotFoundError as e:
            print(f"\nraw_rss2html_file:Error:\n{e}\nPlease correct save file path.")
