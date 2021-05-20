"""This module is needed to work with command-line arguments"""

import argparse
import re

from pathvalidate.argparse import validate_filepath_arg


class Parser:
    """This class is needed to work with command-line arguments"""

    def __init__(self):
        """
        This class constructor initializes the command-line arguments parser
        and calls the method that adds command-line arguments
        """
        self.parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
        self.__add_arguments()

    def __add_arguments(self):
        """This method adds command-line arguments"""
        self.parser.add_argument('source', nargs='?', type=str, help='RSS URL', default=None)
        self.parser.add_argument('--version', help='Print version info', action='version', version=f'Version 0.4')
        self.parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
        self.parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
        self.parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
        self.parser.add_argument('--date', type=validate_date_arg, help='Print cached news for specified date')
        self.parser.add_argument('--to-pdf', type=validate_filepath_arg, help='Converts news to PDF format',
                                 dest='to_pdf')
        self.parser.add_argument('--to-html', type=validate_filepath_arg, help='Converts news to HTML format',
                                 dest='to_html')

    def parse_args(self, argv) -> argparse.Namespace:
        """This method parses command-line arguments and return them"""
        return self.parser.parse_args(argv)


def validate_date_arg(input_value):
    if not len(input_value) == 8 or not re.match('[0-9]{8}', input_value):
        raise argparse.ArgumentTypeError(
            f'Invalid date "{input_value}". The specified date should be in the format "%Y%m%d"')
    return input_value
