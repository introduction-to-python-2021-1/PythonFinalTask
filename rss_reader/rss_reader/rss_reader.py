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
  --date DATE    Print news from local storage for specified day
"""

__version__ = '3.0'

import argparse
import feedparser
import json
import logging
import os
import sys

from urllib.error import URLError
from time import strftime, strptime

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_filename = "log_rss_reader.log"
_storage_filename = "rss_reader_storage.json"
_date_channel_format = '%Y%m%d'
_date_news_format = '%a, %d %b, %Y %I:%M %p'


class RSSReader:
    """Object for parsing command line strings into Python objects.

    Keyword Arguments:
        - source -- RSS URL
        - is_json -- Determines news output in JSON format
        - is_verbose - Determines print logs in stdout
        - limit -- A number of available news
        - date -- Print news from local storage for specified day
    """

    @staticmethod
    def _init_logger(name, is_verbose):
        """Initialization logger object."""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(_log_filename)
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
                 limit=None,
                 date=None):
        """Initialization RSSReader object with arguments from command-line."""
        self.logger = self._init_logger(__name__, is_verbose)
        self.source = source
        self.is_json = is_json
        self.limit = limit
        self.date = date

    @staticmethod
    def _convert_date_format(date, from_format, to_format):
        """Convert date format (for example: from Sun, 23 May, 2021 05:30 PM to 20210523)."""
        format_date = ''
        try:
            format_date = strftime(to_format, strptime(date, from_format))
        except (TypeError, ValueError):
            pass
        return format_date

    def _load_from_storage(self, filename):
        """Load data from local storage."""
        self.logger.info("Load data from local storage...")

        if self.date is None:
            self.logger.warning("Argument 'date' is empty.")
            return

        if not os.path.isfile(filename):
            self.logger.info("Local storage does not exist .")
            return

        with open(filename, 'r') as f:
            try:
                storage_data = json.load(f)
            except (TypeError, ValueError):
                self.logger.error("Failed to load data from local storage.")
                return

            if len(storage_data) == 0:
                self.logger.info("No data in local storage.")
                return

            load_channel = self.source if self.source else ''
            load_news = 0
            data = []

            for index, channel in enumerate(storage_data, start=0):
                if load_channel != '':
                    if channel.get('channel_id', '') != load_channel:
                        continue

                if channel.get('news') is None:
                    continue

                load_channel = {'channel_id': channel.get('channel_id', ''),
                                'channel_title': channel.get('channel_title', ''),
                                'news': [],
                                }

                for news in channel['news']:
                    news_date = self._convert_date_format(news.get('date'), _date_news_format, _date_channel_format)

                    if news_date != self.date:
                        continue

                    load_news += 1
                    load_channel['news'].append(news.copy())

                    if self.limit:
                        if load_news > self.limit:
                            break

                if len(load_channel['news']) > 0:
                    data.append(load_channel)

            if len(data) == 0:
                self.logger.info("No find data in local storage.")
                return

            return data

    def _save_to_storage(self, filename, data):
        """Save data to local storage."""
        self.logger.info("Save data to local storage...")

        if data is None:
            self.logger.warning("Data is None.")
            return

        if len(data) == 0:
            self.logger.warning("Data is empty.")
            return

        storage_data = []

        with open(filename, 'w') as f:
            try:
                storage_data = json.load(f)
            except (TypeError, ValueError):
                self.logger.error("Failed to load data from local storage.")

            storage_channel = {'channel_id': data[0]['channel_id'],
                               'channel_title': data[0]['channel_title'],
                               'news': [news.copy() for news in data[0]['news']]
                               }

            if len(storage_data) == 0:
                storage_data.append(storage_channel)
            else:
                for index, channel in enumerate(storage_data, start=0):
                    if channel.get('channel_id') == self.source:
                        storage_data[index] = storage_channel
                        break

            try:
                json.dump(storage_data, f)
            except (TypeError, ValueError):
                self.logger.error("Failed to save sata to local storage.")

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
    def _format_date(date, to_format):
        """Date formatting (for example: Sun, 23 May, 2021 05:30 PM)."""
        format_date = ''
        try:
            format_date = strftime(to_format, date)
        except TypeError:
            pass
        return format_date

    def _load_data(self, parser):
        """Load data to dict from parser object."""
        self.logger.info("Loading data from RSS...")

        if parser is None:
            self.logger.warning("Parser is None.")
            return

        if parser.feed.get('title', '') == '':
            self.logger.warning("Data is empty.")
            return

        if self.limit:
            feed_entries = parser.entries[: self.limit]
        else:
            feed_entries = parser.entries

        data = [{'channel_id': parser.feed.get('link', self.source),
                 'channel_title': parser.feed.get('title', ''),
                 'news': [{'number': number,
                           'title': entry.get('title', ''),
                           'link': entry.get('link', ''),
                           'author': entry.get('author', ''),
                           'date': self._format_date(entry.get('published_parsed'), _date_news_format),
                           'description': entry.get('summary', ''),
                           }
                          for number, entry in enumerate(feed_entries, start=1)
                          ]
                 }]
        self._save_to_storage(_storage_filename, data)
        return data

    def _print_as_formatted_text(self, data):
        """Print data as formatted text."""
        self.logger.info("Printing data as formatted text...")

        if data is None:
            self.logger.warning("Data is None.")
            return

        if len(data) == 0:
            self.logger.warning("Data is empty.")
            return

        for channel in data:
            print("-" * 100)
            print(f"Channel: {channel.get('channel_title', '')}")

            if channel.get('news') is None:
                continue

            for item in channel['news']:
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

        if len(data) == 0:
            self.logger.warning("Data is empty.")
            return

        json_data = json.dumps(data, indent=4)
        print(json_data)

    def run(self):
        """Load data from RSS and print it in text or json format."""
        if self.date:
            data = self._load_from_storage(_storage_filename)
        else:
            data = self._load_data(self._parse_url())

        if data:
            if self.is_json:
                self._print_as_json(data)
            else:
                self._print_as_formatted_text(data)
        else:
            if self.date:
                print("No find data in local storage")


class SourceAction(argparse.Action):
    """Make 'source' optional if use '--date' argument."""
    def __init__(self, option_strings, dest, with_date=False, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs='?' if with_date else nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def _get_utility_args(argv):
    """Parsing command-line arguments."""
    parser = argparse.ArgumentParser(prog='rss_reader.py', description='Pure Python command-line RSS reader.')
    parser.add_argument('source', action=SourceAction, with_date='--date' in argv[1:], help='RSS URL')
    parser.add_argument('--version', action='version', version=f'"Version {__version__}"', help='Print version info')
    parser.add_argument('--json', action='store_true', default=False, help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', default=False, help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', help='Print news from local storage for specified day')
    return parser.parse_args(argv[1:])


def main():
    """Command-line parsing and run RSS reader utility."""
    # Parse command-line
    args = _get_utility_args(sys.argv)
    # Run utility
    RSSReader(args.source, args.json, args.verbose, args.limit, args.date).run()


if __name__ == "__main__":
    main()
