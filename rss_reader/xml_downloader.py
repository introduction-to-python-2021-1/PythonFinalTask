"""xml_downloader module downloads xml from specified URL address.

Classes:
-------
    XmlDownloader

Attributes:
----------
    _xml: str

Methods:
-------
    __init__(self, html_json_list: list, limit: int = None)
    _download_xml(url: str) -> str
    xml(self) -> str
"""

import requests
import logging


class XmlDownloader:
    """Class XmlDownloader downloads xml from specified URL address and handles errors when necessary.

    Attributes:
    ----------
        _xml: str

    Methods:
    -------
        __init__(self, html_json_list: list, limit: int = None)
            Constructor for XmlDownloader class instance.
        _download_xml(url: str) -> str
            Downloads from specified URL and returns XML as string. Called from the constructor.
        xml(self) -> str
            Getter for self._xml
    """
    def __init__(self, url: str):
        """Constructor for XmlDownloader class instance

        Parameters:
        ----------
        arg1: str
            url - RSS feed URL

        Attributes:
        ----------
        self._xml: str - XML obtained from URL. In case of error - empty string "".
        """
        self._xml = self._download_xml(url)
        if self._xml:
            logging.info(f"XML obtained successfully from {url}")
        else:
            logging.info(f"No XML obtained from {url}")

    @staticmethod
    def _download_xml(url: str) -> str:
        """
        Static method _download_url(url) downloading XML data from RSS feed and handles connection errors.

        Parameters:
        ----------
        arg1: str
            url - RSS feed URL

        Returns:
        -------
        str - XML obtained from URL. In case of error - empty string "".

        Side effects:
        ------------
        Prints to stdout error message when XML data at RSS feed URL not available.
        """
        try:
            response = requests.get(url, stream=True, headers={'user-agent': 'rss_reader/1.4'})
        except Exception as e:
            print(f"RSS feed with URL {url} Not responding\n\nError: {e}")
            return ""

        if response.status_code == 200:
            logging.info(f"Connected to rss feed at: {url}")
            return response.text
        else:
            print(f"Error: RSS feed with URL {url} Not responding. Status code {response.status_code}")
            return ""

    @property
    def xml(self) -> str:
        """property xml() - getter for XML data

        Returns:
        -------
        self._xml: str - XML obtained from URL. In case of error - empty string "".
        """
        return self._xml
