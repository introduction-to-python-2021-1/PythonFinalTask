import unittest

from rssreader.rss_core.rss_classes import RSSItem, RSSNews

rss_item_init_dict = {"title": "-", "link": "-", "pubDate": "-", "guid": "-", "category": "-", "content": ["-"],
                      "description": "-"}
rss_item_str = "Title: -\nDate: -\nLink: -\nCategory: -\nDescription: -\nMedia: ['-']"


class TestRssItem(unittest.TestCase):

    def test_RSSItem_create_from_empty_dict(self):
        RSSItem(**{})

    def test_RSSItem_init(self):
        item = RSSItem(**rss_item_init_dict)
        self.assertEqual(rss_item_str, str(item))

    def test_RSSItem_str(self):
        self.assertEqual(rss_item_str, str(RSSItem(**rss_item_init_dict)))

    def test_RSSItem_as_dict(self):
        self.assertEqual({'Title': '-', 'Date': '-', 'Link': '-', 'Description': '-', 'Category': '-', 'Media': ['-']},
                         RSSItem(**rss_item_init_dict).as_dict())


class TestRssNews(unittest.TestCase):
    def test_RSSNews_create_from_empty_dict(self):
        RSSNews(**{})

    def test_RSSNews_str(self):
        self.assertEqual("\n [link: ]\n\n\nSorry, no news for you...", str(RSSNews(**{})))

    def test_RSSNews_json(self):
        self.assertEqual("""{"Link": "", "Description": "", "Title": "", "News": []}""", RSSNews(**{}).as_json())
