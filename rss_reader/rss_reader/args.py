import argparse


class RssReaderArgs:
    def __init__(self):
        self.__parser = argparse.ArgumentParser(prog='rss_reader', description='Pure Python command-line RSS reader.')
        self.__parser.add_argument(
            '--version',
            # '-v',
            action='version',
            version='%(prog)s 1.2',
            help='Print version info')
        self.__parser.add_argument(
            '--json',
            default=False,
            action='store_true',
            help='Print result as JSON in stdout'
        )
        self.__parser.add_argument(
            '--verbose',
            default=False,
            action='store_true',
            help='Outputs verbose status messages'
        )
        self.__parser.add_argument(
            '--limit',
            type=int,
            help='Limit news topics if this parameter provided')
        self.__parser.add_argument(
            'source',
            # nargs=1,
            type=str,
            help='RSS URL'
        )

        self.args = self.__parser.parse_args()
