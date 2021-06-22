from datetime import date
import os
from .args import RssReaderArgs
import feedparser as fp
import json
from hashlib import md5
from pathlib import Path
import time


class RssReaderApp:
    """main class for application"""

    def run(self):
        """main function to run application"""
        rss_args = RssReaderArgs()
        if not rss_args.args.date and not rss_args.args.source:
            rss_args.print_usage()
            return

        if rss_args.args.verbose:
            self.log = self.__log_stdout
        entries = self.rss_reader(
            source=rss_args.args.source,
            limit=rss_args.args.limit,
        )
        if entries:
            self.print_entries(
                entries,
                json_fmt=rss_args.args.json,
            )

    def log(self, *args):
        """empty method for printing log messages"""
        pass

    def __log_stdout(self, *args):
        """real log method"""
        print(*args)

    def rss_reader(self, source, limit=None):
        """main method for read rss feed"""
        self.log('parsing feed')
        feed = fp.parse(source)
        if 'bozo_exception' in feed:
            self.__log_stdout('Error parsing feed :',
                              feed['bozo_exception'].getMessage())
            return
        self.log('building entries')
        entries = [{
            'title': x.title,
            'link': x.link,
            'summary': self.__get_summary(x),
            'pubdate': time.strftime('%Y%m%d', x.published_parsed)
        } for x in feed.entries[0:limit]]
        return entries

    def __get_summary(self, entry):
        if 'summary' in entry:
            return entry['summary']
        else:
            return ''

    def __source_to_cache_name(self, source):
        cache_name = 'r'+md5(source.lower().encode('utf-8')).hexdigest()
        home = str(Path.home())
        cache_name = os.path.join(home, '.cache', 'rss_reader', cache_name)
        return cache_name

    def make_cache(self, source, entries):
        cache_name = self.__source_to_cache_name(source)
        os.makedirs(os.path.dirname(cache_name), exist_ok=True)
        with open(cache_name, 'w') as outfile:
            json.dump(entries, outfile)
        return cache_name

    def __read_from_cached_json(self, cache_name, date):
        with open(cache_name) as json_file:
            data = json.load(json_file)
        entries = [x for x in data if x['pubdate'] <= date]
        return entries

    def __read_from_cached_source(self, source, date):
        cache_name = self.__source_to_cache_name(source)
        return self.__read_from_cached_json(cache_name, date)

    def read_from_cache(self, source, date):
        if source:
            return self.__read_from_cached_source(source, date)
        else:
            home = str(Path.home())
            cache_folder = os.path.join(home, '.cache', 'rss_reader')
            entries = []
            for src in os.listdir(cache_folder):
                cache_file = os.path.join(cache_folder, src)
                if os.path.isfile(cache_file):
                    entries.extend(
                        self.__read_from_cached_json(cache_file, date))
            return entries

    def print_entries(self, entries, json_fmt=False):
        """print rss entries"""
        self.log('printing entries')
        if json_fmt:
            print(json.dumps(entries))
        else:
            for x in entries:
                print(
                    f"title: {x['title']}\ndate: {x['pubdate']}\nlink: {x['link']}\nsummary: {x['summary']}\n\n")
