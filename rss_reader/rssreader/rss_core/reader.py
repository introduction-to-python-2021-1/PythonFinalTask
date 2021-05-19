"""

    Module stores readers for reading data from given resource
"""
from requests import get
from abc import abstractmethod, ABC

from rssreader.utils import util


class Reader(ABC):
    """

    Abstract class for setting reader for using in Parser
    """

    @abstractmethod
    def get_data(self, source):
        """Get data to be parsed"""


class SiteReader(Reader):
    """

    Class for getting data from site
    """

    def get_data(self, link: str = ""):
        """

        Get data from site and return it
        :param link: link for connecting
        :return: site source
        """
        try:
            response = get(url=link)
            if response.ok:
                content = response.text
                return content
            else:
                raise ValueError("Response from site is not ok! Code:" + str(response.status_code))
        except ValueError as err:
            util.log(show_on_console=True,
                     flag="ERROR",
                     msg=f"ValueError at SiteReader.get_data: {str(err)}")
        except requests.exceptions.RequestException as err:
            util.log(show_on_console=True,
                     flag="ERROR",
                     msg=f"RequestException at SiteReader.get_data: {str(err)}")
