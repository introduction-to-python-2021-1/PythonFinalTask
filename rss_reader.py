#!/usr/bin/env python3
"""
Main module. Receive input info from bash, parse it and print result to stdout.
"""

import argparse
import json as jsn
import logging
import sys

import feedparser


# logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")


def open_rss_link(source, limit, json, verbose):
    content = feedparser.parse(source)

    if verbose:
        logging.basicConfig(stream=sys.stdout)
        logging.info("you ask to print logs")
        print("you ask to print logs")

    if limit and limit <= len(content.entries):
        number_of_news_to_show = limit
    else:
        number_of_news_to_show = len(content.entries)

    if json:
        json_dict = {}
        newslist = []
        newsdict = {}

        for news in content.entries[:number_of_news_to_show]:
            if "title" in news.keys():
                json_dict["Title"] = news.title

            if "summary" in news.keys():
                json_dict["Summary"] = news.summary

            if "description" in news.keys():
                json_dict["Summary"] = news.description

            if "published" in news.keys():
                json_dict["Date"] = news.published

            if "storyimage" in news.keys():
                json_dict["Main_image"] = news.storyimage

            if "media_content" in news.keys():
                json_dict["Image"] = news.media_content

            if "tags" in news.keys():
                if "term" in news.tags:
                    json_dict["Tags"] = news.tags[0]["term"]

            if "link" in news.keys():
                json_dict["News link"] = news.link

            newslist.append(json_dict.copy())

        newsdict["news"] = newslist

        print(jsn.dumps(newsdict))

    else:
        for news in content.entries[:number_of_news_to_show]:
            if "title" in news.keys():
                print(f"Title: {news.title}")

            if "summary" in news.keys():
                print(f"Summary: {news.summary}")
                print("******")

            if "description" in news.keys():
                print(f"Summary: {news.description}")
                print("******")

            if "published" in news.keys():
                print(f"Date: {news.published}")

            if "storyimage" in news.keys():
                print(f"Main_image: {news.storyimage}")

            if "media_content" in news.keys():
                print(f"Image: {news.media_content}")

            if "tags" in news.keys():
                if "term" in news.tags:
                    print(f"Tags: {news.tags[0]}")

            if "link" in news.keys():
                print("------News Link--------")
                print(news.link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader")
    parser.add_argument(
        "--version", action="version", version="Version 1.0", help="Print version info"
    )
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument(
        "--limit", type=int, help="Limit news topics if this parameter provided"
    )
    parser.add_argument(
        "--json", action="store_true", help="Print result as JSON in stdout"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Outputs verbose status messages"
    )

    argum = parser.parse_args()
    open_rss_link(argum.source, argum.limit, argum.json, argum.verbose)
