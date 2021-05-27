from .args import RssReaderArgs
import feedparser as fp
import json


class RssReaderApp:
    """main class for application"""

    def run(self):
        """main function to run application"""
        rss_args = RssReaderArgs()
        if rss_args.args.verbose:
            self.log = self.__log_stdout
        entries = self.rss_reader(
            source=rss_args.args.source,
            limit=rss_args.args.limit,
        )
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
            self.__log_stdout('Error parsing feed :', feed['bozo_exception'].getMessage())
            return
        self.log('building entries')
        entries = [{'title': x.title, 'link': x.link, 'summary': x.summary} for x in feed.entries[0:limit]]
        return entries

    def print_entries(self, entries, json_fmt=False):
        """print rss entries"""
        self.log('printing entries')
        if json_fmt:
            print(json.dumps(entries))
        else:
            for x in entries:
                print(f"title: {x['title']}\nlink: {x['link']}\nsummary: {x['summary']}\n\n")
