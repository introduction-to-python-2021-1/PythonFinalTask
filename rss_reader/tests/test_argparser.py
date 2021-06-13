from argparse import ArgumentParser
from unittest import TestCase

from rss_reader.src.rss_reader import arg_parser


class TestArgparser(TestCase):

    def test_arg_parser(self):
        self.assertIsNotNone(arg_parser())

    def test_arg_parser_instance(self):
        self.assertIsInstance(arg_parser(), ArgumentParser)
