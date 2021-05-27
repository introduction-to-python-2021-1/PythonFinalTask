from .args import RssReaderArgs
import feedparser as fp
import json


class RssReaderApp:
    """main class for application"""

    __verbose = False

    def run(self):
        """main function to run application"""
        rss_args = RssReaderArgs()
        if rss_args.args.verbose:
            self.log = self.__log_stdout
        # log(rss_args.args)
        return self.rss_reader(
            source=rss_args.args.source,
            json_fmt=rss_args.args.json,
            limit=rss_args.args.limit,
        )

    def log(self, *args):
        """empty method for printing log messages"""
        pass

    def __log_stdout(self, *args):
        """real log method"""
        print(*args)

    def rss_reader(self, source, json_fmt=False, limit=None):
        """main method for read rss feed"""
        self.log(f'url: {source}\njson: {json_fmt}\nlimit: {limit}')
        feed = fp.parse(source)
        entries = [{'id': x.id, 'title': x.title, 'link': x.link, 'summary:': x.summary} for x in feed.entries[0:limit]]
        if json_fmt:
            print(json.dumps(entries))
        else:
            for x in entries:
                print(f"title: {x['title']}\nlink: {x['link']}\nsummary: {x['summary']}\n\n")
        return feed.status
