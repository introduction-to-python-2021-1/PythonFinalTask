"""
    Module contains classes RssItem and RssNews
    for working with rss news from different channels
"""
import json
from utils import util


class RssItem:
    """
    Class for storing and processing one piece of rss news
    """

    def __init__(self, **kwargs):
        """
        Constructor for creating rss item

        :param kwargs: named args for filling the class fields.
        It has sens to  passed: title, link, pubDate, guid, description,
        category, media. Other kwargs won't be used. In case
        of absence any of listed parameters class field value will be
        remain its default value ( empty string or empty list for content tag)
        """
        # vars(self).update(kwargs)
        self.title = kwargs.get("title", "")
        self.link = kwargs.get("link", "")
        self.pub_date = kwargs.get("pubDate", "")
        self.guid = kwargs.get("guid", "")
        self.description = kwargs.get("description", "")
        self.category = kwargs.get("category", "")
        self.content = kwargs.get("content", [])

    def __str__(self):
        """
        Convert RssItem to string.

        Title, Date and Link will be included obligatorily.
        Other fields will be ignored if an empty string
         value ( or empty list in case of media tag)
        :return: string
        """
        item_str = f"Title: {self.title}\nDate: {self.pub_date}\nLink: {self.link}"
        if self.category:
            item_str += f"\nCategory: {self.category}"
        if self.description:
            item_str += f"\nDescription: {self.description}"
        if self.content:
            item_str += f"\nMedia: " + str(self.content)

        return item_str

    def as_dict(self):
        """
        Convert RssItem to dict.

        Title, Date and Link will be included obligatorily.
        Other fields will be ignored if an empty string
        value ( or empty list in case of media tag)
        :return: dict
        """
        res_dict = {"Title": self.title, "Date": self.pub_date, "Link": self.link}
        if self.description:
            res_dict["Description"] = self.description
        if self.category:
            res_dict["Category"] = self.category
        if self.content:
            res_dict["Media"] = self.content
        return res_dict


class RssNews:
    """
    Class for getting rss news from site, storing and processing
    """

    def __init__(self, **kwargs):
        """
        Constructor for RssNews
        :param kwargs: should contain link, title, description
        and news for filling corresponding  class fields
        """
        self.link = kwargs.get("link", "")
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.news = kwargs.get("news", [])

    def as_str(self, limit: int = None):
        """
        Convert RssNews to str.

        Title, Date and Link of news provider will be included obligatorily.
        In case of absence of any news, corresponded message will be shown
        :param limit: count of news to be shown. Should be int>0.
        In case of absence or None value all news will be shown
        :return: str
        """
        try:
            news_limit = self._positive_integer_upper_bounded(value=limit, upper_limit=len(self.news))
            news_str = "\n{0} [link: {1}]\n{2}\n\n".format(self.title, self.link,
                                                           f"({self.description})" if self.description else "")
            news_str += "\n\n".join([str(item) for item in self.news[:news_limit]]) if len(self.news) else "No news"
            return news_str
        except (TypeError, ValueError) as err:
            util.log(flag="ERROR", msg=str(err), show_on_console=True)
            exit(1)

    def as_json(self, limit: int = None):
        """
        Convert RssNews to json.
        :return: str in json format
        """
        try:
            news_limit = self._positive_integer_upper_bounded(value=limit, upper_limit=len(self.news))
            news_dict = {"Link": self.link, "Description": self.description, "Title": self.title, "News": []}
            news_dict["News"].extend([news.as_dict() for news in self.news[:news_limit]])
            return json.dumps(news_dict, indent=4)
        except (TypeError, ValueError) as err:
            util.log(flag="ERROR", msg=str(err), show_on_console=True)
            exit(1)

    def _positive_integer_upper_bounded(self, value, upper_limit: int):
        """
        Check value if value is int>0 or None.
        value = upper_limit when value = upper_limit or value is None

        :param value: value for checking and limitation
        :param upper_limit: limit for value. Value can't be greater then upper_limit
        :return: return limited value or throw error if value does't match condition int>0 or None
        """
        if upper_limit is None or upper_limit == 0:
            return 0
        checked_value = value
        if checked_value is None:
            checked_value = upper_limit
        if not isinstance(checked_value, int):
            raise TypeError(f"Limit should be int, but {type(value)} was received")
        if checked_value <= 0:
            raise ValueError(f"Limit should be positive integer, but {value} was received")
        if checked_value > upper_limit:
            checked_value = upper_limit
        return checked_value
