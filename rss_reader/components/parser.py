"""This module is needed to work with command-line arguments"""

import argparse
from datetime import datetime

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
        self.parser.add_argument('--version', help='Print version info', action='version', version=f'Version 0.5')
        self.parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
        self.parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
        self.parser.add_argument('--limit', type=validate_limit_arg,
                                 help='Limit news topics if this parameter provided')
        self.parser.add_argument('--date', type=validate_date_arg, help='Print cached news for specified date')
        self.parser.add_argument('--to-pdf', type=validate_filepath_arg, help='Converts news to PDF format',
                                 dest='to_pdf')
        self.parser.add_argument('--to-html', type=validate_filepath_arg, help='Converts news to HTML format',
                                 dest='to_html')
        self.parser.add_argument('--colorize', help='Print the result of the utility in colorized mode',
                                 action='store_true')

    def parse_args(self, argv) -> argparse.Namespace:
        """
        This method parses command-line arguments and return them

        Parameters:
            argv (list): List of command-line arguments
        """
        return self.parser.parse_args(argv)


def validate_date_arg(input_value) -> str:
    """
    This function checks the format of the argument value --date

    Parameters:
        input_value (str): Argument value --date
    """
    try:
        datetime.strptime(input_value, '%Y%m%d')
    except ValueError:
        raise argparse.ArgumentTypeError(
            f'Invalid date "{input_value}". The specified date does not match the format "%Y%m%d"')
    else:
        return input_value


def validate_limit_arg(input_value) -> int:
    """
    This function checks the format of the argument value --limit

    Parameters:
        input_value (str): Argument value --limit

    """
    try:
        input_value = int(input_value)
    except ValueError:
        raise argparse.ArgumentTypeError(f'The limit argument must be an integer ({input_value} was passed)')
    else:
        if input_value < 1:
            raise argparse.ArgumentTypeError(f'The limit argument must be greater than zero ({input_value} was passed)')
        else:
            return input_value
