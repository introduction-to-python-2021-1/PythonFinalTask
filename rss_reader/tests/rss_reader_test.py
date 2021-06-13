import unittest
from unittest import TestCase, main
import argparse
from rss_reader.rss_reader import create_parser, NewsParser


class ReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wvalue = NewsParser('https://news.yahoo.com/rss/', 5)
        self.default = NewsParser('https://news.yahoo.com/rss/')
        self.wourl = NewsParser('', 5)

    def testdefaultlimit(self):
        self.assertEqual(self.wvalue.limit, self.default.limit)

    def testdefaulturl(self):
        self.assertEqual(self.default.rss, self.wourl.rss)


if __name__ == '__main__':
    main()
