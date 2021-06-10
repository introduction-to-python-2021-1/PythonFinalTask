# Author: Julia Los <los.julia.v@gmail.com>.

"""Python command-line RSS reader

This module is a command-line utility which receives [RSS] URL and prints results in human-readable format.

Utility provides the following interface:
rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE]
                                                    [--to-fb2 FILE] [--to-html FILE] [--colorize] source

Positional arguments:
  source         RSS URL

Optional arguments:
  -h, --help     Show help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Print news from local storage for specified day
  --to-fb2       Save result to file in fb2 format
  --to-html      Save result to file in html format
  --colorize     Print result in colorized mode
"""

__version__ = '5.0'

import argparse
import colorama
import feedparser
import json
import logging
import sys

from .local_storage import _date_news_format, load_from_storage, save_to_storage
from .save_to_file import save_to_fb2, save_to_html
from termcolor import colored
from time import strftime
from urllib.error import URLError

_log_format = "%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_filename = "log_rss_reader.log"
_storage_filename = "rss_reader_storage.json"


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


def parse_url(source, logger=None):
    """Parse RSS URL and return parser object."""
    if logger:
        logger.info("Parsing RSS URL...")

    if not source or source == '':
        if logger:
            logger.error("Source is empty.")
        sys.exit("RSS URL is incorrect.")

    try:
        parser = feedparser.parse(source)
    except URLError:
        if logger:
            logger.error("RSS URL is incorrect.", exc_info=True)
        sys.exit("RSS URL is incorrect.")

    if parser.get('encoding') == '':
        if logger:
            logger.error("Feed’s character encoding is incorrect.")
        sys.exit("RSS URL is incorrect.")

    if parser.feed.get('title', '') == '':
        if logger:
            logger.error("Feed’s title is empty.")
        sys.exit("RSS URL is incorrect.")

    return parser


def format_date(date, to_format):
    """Date formatting (for example: Sun, 23 May, 2021 05:30 PM)."""
    formatted_date = ''
    try:
        formatted_date = strftime(to_format, date)
    except TypeError:
        pass
    return formatted_date


def get_image_link(entry):
    """Get image link from parser object."""
    image_link = ''
    # image in <enclosure> tag
    if entry.get('links'):
        for link in entry.get('links'):
            link_type = link.get('type', 'image/jpeg')
            link_href = link.get('href', '')

            if link_type == 'image/jpeg' and link_href != '':
                return link_href

    # image in <figure> tag
    if entry.get('img'):
        content_source = entry.get('img').get('src', '')

        if content_source != '':
            return content_source

    # image in <media:content> tag
    if entry.get('media_content'):
        for link in entry.get('media_content'):
            link_type = link.get('type', 'image/jpeg')
            link_href = link.get('url', '')

            if link_type == 'image/jpeg' and link_href != '':
                return link_href

    return image_link


def load_data(parser, load_source, limit=None, logger=None):
    """Load data to dict from parser object."""
    if logger:
        logger.info("Loading data from RSS...")

    if parser is None:
        if logger:
            logger.warning("Parser is None.")
        return

    if parser.feed.get('title', '') == '':
        if logger:
            logger.warning("Data is empty.")
        return

    data = [{'channel_id': load_source,
             'channel_title': parser.feed.get('title', ''),
             'news': [{'number': number,
                       'title': entry.get('title', ''),
                       'link': entry.get('link', ''),
                       'author': entry.get('author', ''),
                       'date': format_date(entry.get('published_parsed'), _date_news_format),
                       'image': get_image_link(entry),
                       'description': entry.get('summary', ''),
                       }
                      for number, entry in enumerate(parser.entries, start=1)
                      ]
             }]
    save_to_storage(_storage_filename, data, logger)

    if limit:
        if len(data[0]['news']) > limit:
            data[0]['news'] = data[0]['news'][: limit]

    return data


def _colorize_text(is_colorize, text, *args, **kwargs):
    """Colorize text if needed."""
    if is_colorize:
        return colored(text, *args, **kwargs)
    else:
        return text


def print_as_formatted_text(data, is_colorize=False, logger=None):
    """Print data as formatted text."""
    if logger:
        logger.info("Printing data as formatted text...")

    if data is None:
        if logger:
            logger.warning("Data is None.")
        return

    if len(data) == 0:
        if logger:
            logger.warning("Data is empty.")
        return

    for channel in data:
        print("-" * 100)
        print(_colorize_text(is_colorize, f"Channel: {channel.get('channel_title', '')}",
                             'white', 'on_blue', attrs=['bold']))

        if channel.get('news') is None:
            continue

        for item in channel['news']:
            print("-" * 100)
            print(_colorize_text(is_colorize, f"News № {item.get('number', '')}", 'cyan', attrs=['bold']))
            print(_colorize_text(is_colorize, "Title:", 'red') + f" {item.get('title', '')}")
            print(_colorize_text(is_colorize, "Link:", 'yellow') + f" {item.get('link', '')}")

            if item.get('author', '') != '':
                print(_colorize_text(is_colorize, "Author:", 'cyan') + f" {item['author']}")

            if item.get('date', '') != '':
                print(_colorize_text(is_colorize, "Date:", 'green') + f" {item['date']}")

            if item.get('image', '') != '':
                print(_colorize_text(is_colorize, "Image:", 'magenta') + f" {item['image']}")

            if item.get('description', '') != '':
                print(_colorize_text(is_colorize, f"{item['description']}", 'green'))


def print_as_json(data, is_colorize=False, logger=None):
    """Print data as JSON."""
    if logger:
        logger.info("Printing data as JSON...")

    if data is None:
        if logger:
            logger.warning("Data is None.")
        return

    if len(data) == 0:
        if logger:
            logger.warning("Data is empty.")
        return

    json_data = json.dumps(data, indent=4)

    if is_colorize:
        print_lines = []
        colorize_words = {'"channel_id":': ['white', 'on_cyan'],
                          '"channel_title":': ['white', 'on_blue'],
                          '"news":': ['white', 'on_magenta'],
                          '"number":': ['cyan'],
                          '"title":': ['red'],
                          '"link":': ['yellow'],
                          '"author":': ['cyan'],
                          '"date":': ['green'],
                          '"image":': ['magenta'],
                          '"description":': ['green'],
                          }

        for line in json_data.splitlines():
            for word, color_attr in colorize_words.items():
                if line.find(word) >= 0:
                    print_lines.append(line.replace(word, _colorize_text(is_colorize, word, *color_attr)))
                    break
            else:
                print_lines.append(line)

        json_data = "\n".join(print_lines)

    print(json_data)


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
    parser.add_argument('--to-fb2', metavar='FILE', dest='to_fb2', help='Save result to file in fb2 format')
    parser.add_argument('--to-html', metavar='FILE', dest='to_html', help='Save result to file in html format')
    parser.add_argument('--colorize', action='store_true', default=False, help='Print result in colorized mode')
    return parser.parse_args(argv[1:])


def main():
    """Command-line parsing and run RSS reader utility."""
    # Parse command-line
    args = _get_utility_args(sys.argv)

    # Initialization logger object
    logger = _init_logger('rss_reader.__main__', args.verbose)

    # Load data from RSS URL or local storage
    if args.date and not args.source:
        print_data = load_from_storage(_storage_filename, args.date, '', args.limit, logger)
    else:
        parser = parse_url(args.source, logger)
        load_source = parser.feed.get('link', args.source) if parser else args.source

        if args.date:
            print_data = load_from_storage(_storage_filename, args.date, load_source, args.limit, logger)
        else:
            print_data = load_data(parser, load_source, args.limit, logger)

    if not print_data:
        sys.exit("No find data in local storage." if args.date else "")

    if args.colorize:
        colorama.init()

    # Print result in stdout
    if args.json:
        print_as_json(print_data, args.colorize, logger)
    else:
        print_as_formatted_text(print_data, args.colorize, logger)

    if args.colorize:
        colorama.deinit()

    # Save result to fb2 file
    if args.to_fb2:
        save_to_fb2(args.to_fb2, print_data, logger)

    # Save result to html file
    if args.to_html:
        save_to_html(args.to_html, print_data, logger)


if __name__ == "__main__":
    main()
