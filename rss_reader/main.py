import json
import logging
import ssl
import sys
from sqlite3 import IntegrityError

import feedparser
from dateutil.parser import parse, ParserError

from rss_reader.db import DB
from rss_reader.parser import parse_args

db_obj = DB()

ssl._create_default_https_context = ssl._create_unverified_context


def parse_feed(source):
    """Try to parse feed and return it"""
    result = feedparser.parse(source)
    logging.info(f"Starting parse {source}")
    if not result.entries:
        logging.error(f"Unable to parse source {source}. Error: {e}")
        exit(1)
    else:
        return feedparser.parse(source)


def get_content(source):
    feed = parse_feed(source)
    content = []
    for entry in feed.entries:
        try:
            image_url = entry.media_content[0]["url"]
        except Exception:
            #  if no image in media content then image is None
            image_url = None
        pubdate = parse(entry.published).date()
        title = entry.title
        link = entry.link
        content.append({
            "source": source,
            "pubdate": str(pubdate),
            "title": title,
            "image_url": image_url,
            "link": link
        })

    if len(content) < 1:
        logging.error("Length of your feed = 0, try correct link or choose another rss-feed")
        exit(1)
    return content


def format_news_to_print(content):
    #  if image: None skip it
    content = [{key: value for key, value in news.items() if value and key != "image_path"} for news in content]
    return content


def print_news(content, json_state):
    content = format_news_to_print(content)
    if json_state:
        print_news_json(content)
    else:
        for news in content:
            print("\n".join([f"{key}: {value}" for key, value in news.items()]), "\n")


def print_news_json(content):
    content = format_news_to_print(content)
    print(json.dumps(content, indent=4))


def cache_news(content):
    for news in content:
        try:
            db_obj.add_news(news=tuple(news.values()))
        #  The error will occur if the database contains news with the following link
        except IntegrityError:
            continue
    logging.info("News was cached")


def get_news_from_cache(pubdate, source):
    """
        Prints news for the date.
        Parameters:
            source=URL of rss-feed: optional
            pubdate=Date
        Return the list of dicts with news parameters(pubdate, title, link, image(url))
    """
    #  correct date from 20210221 to 2021-02-21
    try:
        pubdate = parse(pubdate).date()
        content = db_obj.select_news_from_cache(rss_source=source, pubdate=str(pubdate))
        if not content:
            logging.error("No news with this date")
            exit(1)
        else:
            return content
    except ParserError:
        logging.error("Your date is incorrect")
        exit(1)


def main():
    db_obj.create_schema()

    args = parse_args(sys.argv[1:])
    logging.basicConfig(level=logging.INFO if args.verbose else logging.ERROR)

    if args.date:
        content = get_news_from_cache(pubdate=args.date, source=args.source)
    else:
        content = get_content(source=args.source)
        cache_news(content)

    if args.limit < 1 or args.limit > len(content):
        logging.warning("Limit is set by default = length feed")
        args.limit = len(content)
    content = content[:args.limit]
    print_news(content=content, json_state=args.json)


if __name__ == "__main__":
    main()
