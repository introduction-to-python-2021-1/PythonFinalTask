import unittest
from rss_reader.reader import Article

"""Test cases to test Article methods"""


class TestArticle(unittest.TestCase):
    def setUp(self):
        self.article = Article('title', 'link', '2021-05-21T15:03:25Z', 'source', 'description', 'image')

    def test_date_str(self):
        self.assertEqual(self.article.date.strftime("%a, %d %B, %Y"), 'Fri, 21 May, 2021')

    def test_to_dict(self):
        self.assertEqual(self.article.to_dict(), {
            'Title': 'title',
            'Link': 'link',
            'Date': 'Fri, 21 May, 2021',
            'Source': 'source',
            'Description': 'description',
            'Image': 'image',
        })


if __name__ == "__main__":
    unittest.main()
