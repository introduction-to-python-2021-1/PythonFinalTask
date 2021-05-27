"""
    Module stores readers for reading data from given resource
"""
import requests
from abc import abstractmethod, ABC

from utils import util


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

    def get_data(self, link: str):
        """
        Get data from site and return it
        :param link: link for connecting
        :return: site source
        """
        try:
            if not link.startswith(("https://", "http://")):
                util.log(show_on_console=True,
                         flag="ERROR",
                         msg=f"Can't get data from site: Link should starts with http:// or https://")
                exit(1)
            response = requests.get(url=link)
            response.encoding = 'utf-8'
            if response.ok:
                content = response.text
                return content
            else:
                raise ConnectionError(f"Response from site is not ok! Response code: {response.status_code}")
        except ValueError:
            util.log(show_on_console=True,
                     flag="ERROR",
                     msg=f"Value error has occurred while getting data from chanel")
            exit(1)
        except requests.exceptions.RequestException:
            util.log(show_on_console=True,
                     flag="ERROR",
                     msg=f"Request error has occurred while getting data from chanel")
            exit(1)
