"""

    Module contains classes RSSItem and RSSNews
    for working with rss news from different channels
"""
import json


class RSSItem:
    """

    Class for storing and processing one piece of rss news
    """
    title = ""
    link = ""
    pubDate = ""
    guid = ""
    description = ""
    category = ""
    content = []

    def __init__(self, **kwargs):
        """

        Constructor for creating rss item

        :param kwargs: named args for filling the class fields.
        It has sens to  passed: title, link, pubDate, guid, description,
        category, media. Other kwargs won't be used. In case
        of absence any of listed parameters class field value will be
        remain its default value ( empty string or empty list for media tag)
        """
        vars(self).update(kwargs)

    def __str__(self):
        """

        Convert RSSItem to string.

        Title, Date and Link will be included obligatorily.
        Other fields will be ignored if an empty string
         value ( or empty list in case of media tag)
        :return: string
        """
        res_str = "Title: " + self.title + "\nDate: " + self.pubDate + "\nLink: " + self.link
        if self.category:
            res_str += "\nCategory: " + self.category
        if self.description:
            res_str += "\nDescription: " + self.description
        if self.content:
            res_str += "\nMedia: " + str(self.content)

        return res_str

    def as_dict(self):
        """

        Convert RSSItem to dict.

        Title, Date and Link will be included obligatorily.
        Other fields will be ignored if an empty string
        value ( or empty list in case of media tag)
        :return: dict
        """
        res_dict = {"Title": self.title, "Date": self.pubDate, "Link": self.link}
        if self.description:
            res_dict["Description"] = self.description
        if self.category:
            res_dict["Category"] = self.category
        if self.content:
            res_dict["Media"] = self.content
        return res_dict


class RSSNews:
    """
    
    Class for getting rss news from site, storing and processing
    """
    link = ""
    title = ""
    description = ""
    news = []

    def __init__(self, **kwargs):
        """

        Constructor for RSSNews
        
        :param kwargs: should contain link, title, description
        and news for filling corresponding  class fields
        """
        self.link = kwargs.get("link", "")
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.news = kwargs.get("news", "")

    def __str__(self):
        """

        Convert RSSNews to str.

        Title, Date and Link of news provider will be included obligatorily.
        In case of absence of any news, corresponded message will be shown
        :return: str
        """
        res_str = "\n{0} [link: {1}]\n{2}\n\n".format(self.title, self.link,
                                                      f"({self.description})" if self.description else "")
        res_str += "\n\n".join([str(item) for item in self.news]) if len(self.news) else "Sorry, no news for you..."

        return res_str

    def as_json(self):
        """

        Convert RSSNews to json.

        :return: str in json format
        """
        news_dict = {"Link": self.link, "Description": self.description, "Title": self.title, "News": []}
        news_dict["News"].extend([news.as_dict() for news in self.news])
        return json.dumps(news_dict)
