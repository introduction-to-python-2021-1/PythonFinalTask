import feedparser
import argparse
import json
import unidecode
import logging
import sys


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='url of rss', type=str)
    parser.add_argument('--limit', help='Limit news topics if this parameter provided', type=int)
    parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    parser.add_argument('--version', help='Print version info', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    return parser


class NewsParser:
    def __init__(self, rss=None, limit=None, verbose=False):
        self.verbose = verbose
        if rss:
            self.rss = rss
        else:
            self.rss = 'https://news.yahoo.com/rss/'
            if verbose:
                logging.warning('default url has been set')
        if limit:
            if 40 > limit > 0:
                self.limit = limit
            else:
                self.limit = 29
                if verbose:
                    logging.warning('default limit border has been set')
        else:
            self.limit = 5
            if verbose:
                logging.warning('default limit value has been set')

    def get_posts_details(self):

        if self.rss and self.limit:

            blog_feed = feedparser.parse(self.rss)

            # getting lists of blog entries via .entries
            posts = blog_feed.entries[:self.limit]

            # dictionary for holding posts details
            posts_details = {'Blog title': blog_feed.feed.title,
                             'Blog link': blog_feed.feed.link,
                             'Blog date': blog_feed.feed.published,
                             'Blog image': blog_feed.feed.image.href}
            if self.verbose:
                logging.warning('Created header')
            post_list = []

            # iterating over individual posts
            for post in posts:
                temp = dict()

                # if any post doesn't have information then throw error.
                try:
                    temp['title'] = unidecode.unidecode(post.title)
                    temp['link'] = post.link
                    temp['date'] = post.published
                    temp['img'] = post.media_content.url
                except:
                    pass

                post_list.append(temp)

            # storing lists of posts in the dictionary
            posts_details['posts'] = post_list

            return posts_details  # returning the details which is dictionary
        else:
            return None


class NewsOutput:
    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            self.data = []

    def save_json(self):
        with open('out.json', 'w') as textout:
            json.dump(self.data, textout, indent=4)

    def output(self):
        print(json.dumps(self.data, indent=4))


def main():
    argparser = create_parser()
    args = argparser.parse_args()

    if args.version:
        print('1.1.5')
        exit()

    feed_url = args.url
    limit = args.limit
    stdout = args.json
    verbose = args.verbose

    newsParser = NewsParser(feed_url, limit, verbose)
    data = newsParser.get_posts_details()  # return blogs data as a dictionary

    newsOutput = NewsOutput(data)
    newsOutput.output()
    if verbose:
        logging.warning('News outputted in console')
    if stdout:
        newsOutput.save_json()
        if verbose:
            logging.warning('News outputted in file')
