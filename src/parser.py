"""This module is needed to work with command-line arguments"""

import argparse


class Parser:
    """This class is needed to work with command-line arguments"""

    def __init__(self):
        """This class constructor initializes the command-line arguments parser
        and calls the method that adds command-line arguments"""
        self.parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
        self.__add_arguments()

    def __add_arguments(self):
        """
        This method adds command-line arguments
        :return: None
        """
        self.parser.add_argument('source', type=str, help='RSS URL')
        self.parser.add_argument('--version', help='Print version info', action='version', version='Version 0.1')
        self.parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
        self.parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
        self.parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    def parse_args(self):
        """
        This method parses command-line arguments and return them
        :return: argparse
        """
        return self.parser.parse_args()
