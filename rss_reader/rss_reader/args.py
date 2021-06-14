import argparse
from datetime import datetime


class RssReaderArgs:
    """class for command line arguments parsing"""

    def __init__(self, argv=None):
        self.__parser = argparse.ArgumentParser(
            prog='rss_reader', description='Pure Python command-line RSS reader.')
        self.__parser.add_argument(
            '--version', action='version', version='%(prog)s version 1.3', help='Print version info')
        self.__parser.add_argument(
            '--json', default=False, action='store_true', help='Print result as JSON in stdout')
        self.__parser.add_argument(
            '--verbose', default=False, action='store_true', help='Outputs verbose status messages')
        self.__parser.add_argument(
            '--limit', type=int, help='Limit news topics if this parameter provided')
        self.__parser.add_argument(
            '--date', type=lambda d: datetime.strptime(d, '%Y%m%d'), help='Get feed from cache by date fmt=%%Y%%m%%d')
        self.__parser.add_argument(
            'source',
            type=str,
            nargs='?',
            default='',
            help='RSS URL'
        )
        self.args = self.__parser.parse_args(argv)

    def print_usage(self):
        self.__parser.print_usage()
