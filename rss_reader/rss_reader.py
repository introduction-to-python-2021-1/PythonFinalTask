# Author: Julia Los <los.julia.v@gmail.com>.

"""Python command-line RSS reader

This module is a command-line utility which receives [RSS] URL and prints results in human-readable format.

Utility provides the following interface:
rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

Positional arguments:
  source         RSS URL

Optional arguments:
  -h, --help     Show help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
"""

__version__ = '2.0'

import argparse
import feedparser
import json
import logging

from urllib.error import URLError
from time import strftime

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


class RSSReader:
    """Object for parsing command line strings into Python objects.

    Keyword Arguments:
        - source -- RSS URL
        - is_json -- Determines news output in JSON format
        - is_verbose - Determines print logs in stdout
        - limit -- A number of available news
    """

    @staticmethod
    def _init_logger(name, is_verbose):
        """Initialization logger object."""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler("log_rss_reader.log")
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(_log_format))
        logger.addHandler(handler)

        if is_verbose:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            handler.setFormatter(logging.Formatter(_log_format))
            logger.addHandler(handler)

        return logger

    def __init__(self,
                 source=None,
                 is_json=False,
                 is_verbose=False,
                 limit=None):
        """Initialization RSSReader object with arguments from command-line."""
        self.logger = self._init_logger(__name__, is_verbose)
        self.source = source
        self.is_json = is_json
        self.limit = limit

    def _parse_url(self):
        """Parse RSS URL and return parser object."""
        self.logger.info("Parsing RSS URL...")

        if not self.source or self.source == '':
            self.logger.error("Source is empty.")
            return

        try:
            parser = feedparser.parse(self.source)
        except URLError:
            self.logger.error("RSS URL is incorrect.", exc_info=True)
            return

        if parser.get('encoding') == '':
            self.logger.error("Feed’s character encoding is incorrect.", exc_info=True)
            return

        return parser

    @staticmethod
    def _format_date(date):
        """Date formatting (for example: Sun, 23 May, 2021 05:30 PM) ."""
        format_date = ''
        try:
            format_date = strftime('%a, %d %b, %Y %I:%M %p', date)
        except TypeError:
            pass
        return format_date

    def _load_data(self, parser):
        """Load data to dict from parser object."""
        self.logger.info("Loading data from RSS...")

        if parser is None:
            self.logger.warning("Parser is None.")
            return

        if parser.feed.get('title') is None:
            self.logger.warning("Channel is empty.")
            return

        data = {'channel': parser.feed.get('title', '')}

        if self.limit:
            feed_entries = parser.entries[: self.limit]
        else:
            feed_entries = parser.entries

        data['news'] = [{'number': number,
                         'title': entry.get('title', ''),
                         'link': entry.get('link', ''),
                         'author': entry.get('author', ''),
                         'date': self._format_date(entry.get('published_parsed')),
                         'description': entry.get('summary', ''),
                         }
                        for number, entry in enumerate(feed_entries, start=1)
                        ]
        return data

    def _print_as_formatted_text(self, data):
        """Print data as formatted text."""
        self.logger.info("Printing data as formatted text...")

        if data is None:
            self.logger.warning("Data is None.")
            return

        if data.get('channel', '') == '':
            self.logger.warning("Channel is empty.")
            return

        print("-" * 100)
        print(f"Channel: {data['channel']}")

        if data.get('news') is None:
            self.logger.warning("Channel don't have news.")
            return

        for item in data['news']:
            print("-" * 100)
            print(f"News № {item.get('number', '')}")
            print(f"Title: {item.get('title', '')}")
            print(f"Link: {item.get('link', '')}")

            if item.get('author', '') != '':
                print(f"Author: {item['author']}")

            if item.get('date', '') != '':
                print(f"Date: {item['date']}")

            if item.get('description', '') != '':
                print(f"\n{item['description']}")

    def _print_as_json(self, data):
        """Print data as JSON."""
        self.logger.info("Printing data as JSON...")
        if data is None:
            self.logger.warning("Data is None.")
            return

        if data.get('channel', '') == '':
            self.logger.warning("Channel is empty.")
            return

        json_data = json.dumps(data, indent=4)
        print(json_data)

    def run(self):
        """Load data from RSS and print it in text or json format."""
        data = self._load_data(self._parse_url())

        if data:
            if self.is_json:
                self._print_as_json(data)
            else:
                self._print_as_formatted_text(data)


def main():
    """Command-line parsing and run RSS reader utility."""
    # Parse command-line
    parser = argparse.ArgumentParser(prog='rss_reader.py', description='Pure Python command-line RSS reader.')
    parser.add_argument('source', help='RSS URL')
    parser.add_argument('--version', action='version', version=f'"Version {__version__}"', help='Print version info')
    parser.add_argument('--json', action='store_true', default=False, help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', default=False, help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    args = parser.parse_args()
    # Run utility
    RSSReader(args.source, args.json, args.verbose, args.limit).run()


if __name__ == "__main__":
    main()
