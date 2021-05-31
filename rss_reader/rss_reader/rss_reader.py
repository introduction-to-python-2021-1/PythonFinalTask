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
  --to-fb2       Save result to file in fb2 format
  --to-html      Save result to file in html format
"""

__version__ = '4.0'

import argparse
import feedparser
import jinja2
import json
import logging
import os
import sys
import xml.etree.ElementTree as et

from contextlib import suppress
from datetime import datetime
from time import strftime, strptime
from urllib.error import URLError

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_filename = "log_rss_reader.log"
_storage_filename = "rss_reader_storage.json"
_date_channel_format = '%Y%m%d'
_date_news_format = '%a, %d %b, %Y %I:%M %p'
_html_template = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">          
    <title>{{ title }}</title>
  </head>
  <body>
    <h1 align="center">{{ title }}</h1>
    {% for channel in data %}
    <div id={{ channel.channel_id }}>
      <h2 align="center">{{ channel.channel_title }}</h2>
      {% if channel.news %}     
      {%- for item in channel.news %}
      <div>
        <h3>News № {{ item.number }}</h3>
        <p><b>Title:</b> {{ item.title }}</p>
        <p><b>Link:</b> <a href={{ item.link }}>{{ item.link }}</a></p>
        {% if item.author %}
        <p><b>Author:</b> {{ item.author }}</p>
        {%- endif %}
        {% if item.date %}
        <p><b>Date:</b> {{ item.date }}</p>
        {%- endif %}                  
        {% if item.image %}
        <img src={{ item.image }} width="600" height="400">
        {%- endif %}                   
        {% if item.description %}
        <p>{{ item.description }}</p>
        {%- endif %}
      </div>                   
      {% endfor %}
      {% endif %}
    </div>
    {% endfor %}
  </body>
</html>"""


class RSSReader:
    """Object for parsing command line strings into Python objects.

    Keyword Arguments:
        - source -- RSS URL
        - is_json -- Determines news output in JSON format
        - is_verbose - Determines print logs in stdout
        - limit -- A number of available news
        - date -- Print news from local storage for specified day
        - to_fb2 -- Save result to file in fb2 format
        - to-html -- Save result to file in html format
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
                 date=None,
                 to_fb2=None,
                 to_html=None):
        """Initialization RSSReader object with arguments from command-line."""
        self.logger = self._init_logger(__name__, is_verbose)
        self.source = source
        self.is_json = is_json
        self.limit = limit
        self.date = date
        self.to_fb2 = to_fb2
        self.to_html = to_html

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
            self.logger.info("Local storage does not exist.")
            return

        with suppress(OSError):
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

        with suppress(OSError):
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
                    self.logger.error("Failed to save data to local storage.")

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

    @staticmethod
    def _get_image_link(entry):
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

    def _load_data(self, parser):
        """Load data to dict from parser object."""
        self.logger.info("Loading data from RSS...")

        if parser is None:
            self.logger.warning("Parser is None.")
            return

        if parser.feed.get('title', '') == '':
            self.logger.warning("Data is empty.")
            return

        data = [{'channel_id': parser.feed.get('link', self.source),
                 'channel_title': parser.feed.get('title', ''),
                 'news': [{'number': number,
                           'title': entry.get('title', ''),
                           'link': entry.get('link', ''),
                           'author': entry.get('author', ''),
                           'date': self._format_date(entry.get('published_parsed'), _date_news_format),
                           'image': self._get_image_link(entry),
                           'description': entry.get('summary', ''),
                           }
                          for number, entry in enumerate(parser.entries, start=1)
                          ]
                 }]
        self._save_to_storage(_storage_filename, data)

        if self.limit:
            if len(data[0]['news']) > self.limit:
                data[0]['news'] = data[0]['news'][: self.limit]

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

                if item.get('image', '') != '':
                    print(f"Image: {item['image']}")

                if item.get('description', '') != '':
                    print(f"{item['description']}")

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

    @staticmethod
    def _check_filename(filename, extent):
        """Check if the filename is correct."""
        if filename is None:
            return

        if filename == '':
            return

        root, ext = os.path.splitext(filename)

        if ext == '':
            if os.path.basename(filename) == '':
                return

            return filename + extent
        else:
            if ext != extent:
                return

            return filename

    def _save_to_fb2(self, filename, data):
        """Save data to file in fb2 format."""
        self.logger.info("Save data to file in fb2 format...")

        filename = self._check_filename(filename, '.fb2')

        if filename is None:
            self.logger.warning("Filename is incorrect.")
            return

        if data is None:
            self.logger.warning("Data is None.")
            return

        if len(data) == 0:
            self.logger.warning("Data is empty.")
            return

        xml_root = et.Element('FictionBook', {'xmlns': "http://www.gribuser.ru/xml/fictionbook/2.0",
                                              'xmlns:l': "http://www.w3.org/1999/xlink"})
        # description
        xml_description = et.SubElement(xml_root, 'description')
        # description - title info
        xml_title_info = et.SubElement(xml_description, 'title-info')
        et.SubElement(xml_title_info, 'genre').text = 'comp_soft'
        xml_author = et.SubElement(xml_title_info, 'author')
        et.SubElement(xml_author, 'nickname').text = 'RSSReader'
        et.SubElement(xml_author, 'email').text = 'RSSReader@gmail.com'
        et.SubElement(xml_title_info, 'book-title').text = 'RSS Reader utility results'
        xml_annotation = et.SubElement(xml_title_info, 'annotation')
        xml_p = et.SubElement(xml_annotation, 'p')
        xml_p.text = 'News found by RSS Reader utility.'
        day_create = datetime.today()
        xml_date = et.SubElement(xml_title_info, 'date', {'value': day_create.strftime("%Y-%m-%d")})
        xml_date.text = day_create.strftime("%d %B, %Y")
        et.SubElement(xml_title_info, 'lang').text = 'en'
        # description - document info
        xml_document_info = et.SubElement(xml_description, 'document-info')
        xml_author = et.SubElement(xml_document_info, 'author')
        et.SubElement(xml_author, 'first-name').text = 'Larina'
        et.SubElement(xml_author, 'last-name').text = 'Fox'
        et.SubElement(xml_author, 'email').text = 'LarinaFox@gmail.com'
        et.SubElement(xml_document_info, 'program-used').text = 'RSSReader 4.0'
        et.SubElement(xml_document_info, 'date', {'value': '2021-05-29'}).text = '29 May, 2021'
        et.SubElement(xml_document_info, 'id').text = '2021_05_29_18_00_00'
        et.SubElement(xml_document_info, 'version').text = '1.0'
        xml_history = et.SubElement(xml_document_info, 'history')
        et.SubElement(xml_history, 'p').text = '1.0 - preparation fb2'
        # body
        xml_body = et.SubElement(xml_root, 'body')
        xml_title = et.SubElement(xml_body, 'title')
        et.SubElement(xml_title, 'p').text = 'RSS Reader utility results'
        xml_main_section = et.SubElement(xml_body, 'section')

        for channel in data:
            xml_channel = et.SubElement(xml_main_section, 'section', {'id': channel.get('channel_id', '')})
            et.SubElement(xml_channel, 'title').text = channel.get('channel_title', '')

            if channel.get('news') is None:
                continue

            for item in channel['news']:
                xml_news = et.SubElement(xml_channel, 'section')
                et.SubElement(xml_news, 'p').text = f"News № {item.get('number', '')}"
                et.SubElement(xml_news, 'p').text = f"Title: {item.get('title', '')}"
                xml_news_link = et.SubElement(xml_news, 'p')
                xml_news_link.text = 'Link: '
                xml_news_link_a = et.SubElement(xml_news_link, 'a', {'l:href': item.get('link', '')})
                xml_news_link_a.text = item.get('link', '')

                if item.get('author', '') != '':
                    et.SubElement(xml_news, 'p').text = f"Author: {item['author']}"

                if item.get('date', '') != '':
                    et.SubElement(xml_news, 'p').text = f"Date: {item['date']}"

                if item.get('image', '') != '':
                    et.SubElement(xml_news, 'image', {'l:href': item.get('image', '')})

                if item.get('description', '') != '':
                    et.SubElement(xml_news, 'p').text = f"\n{item['description']}"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                xml_tree = et.ElementTree(xml_root)
                et.indent(xml_tree)
                xml_tree.write(f, encoding="unicode", xml_declaration=True)
        except OSError:
            self.logger.error('Failed to save data to fb2 file.')

    def _save_to_html(self, filename, data):
        """Save data to file in html format."""
        self.logger.info("Save data to file in html format...")

        filename = self._check_filename(filename, '.html')

        if filename is None:
            self.logger.warning("Filename is incorrect.")
            return

        if data is None:
            self.logger.warning("Data is None.")
            return

        if len(data) == 0:
            self.logger.warning("Data is empty.")
            return

        environment = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
        template = environment.from_string(_html_template)
        html_text = template.render(title="RSS Reader utility results", data=data)

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_text)
        except OSError:
            self.logger.error('Failed to save data to html file.')

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

            if self.to_fb2:
                self._save_to_fb2(self.to_fb2, data)

            if self.to_html:
                self._save_to_html(self.to_html, data)
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
    parser.add_argument('--to-fb2', metavar='FILE', dest='to_fb2', help='Save result to file in fb2 format')
    parser.add_argument('--to-html', metavar='FILE', dest='to_html', help='Save result to file in html format')
    return parser.parse_args(argv[1:])


def main():
    """Command-line parsing and run RSS reader utility."""
    # Parse command-line
    args = _get_utility_args(sys.argv)
    # Run utility
    RSSReader(args.source, args.json, args.verbose, args.limit, args.date, args.to_fb2, args.to_html).run()


if __name__ == "__main__":
    main()
