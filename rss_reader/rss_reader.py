"""
Main module. Receive input info from bash, parse it and print result to stdout.
"""

import argparse
import json as jsn
import logging
import logging.handlers
import sys
from urllib.error import URLError

import feedparser

NEWS_PARTS = ["title", "published", "summary", "description", "storyimage", "media_content", "link"]


def set_logger(verbose):
    # Choose the output for logs and configure a logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout), ] if verbose else [logging.FileHandler("logs.log"), ]
    )
    logger = logging.getLogger()
    return logger


def printing_parsing_news(content, number_of_news_to_show):
    # Print news to stdout
    for news in content.entries[:number_of_news_to_show]:
        for item in NEWS_PARTS:
            if item in news.keys():
                print(item.capitalize() + ": " + str(news[item]))
        print("***************\n")


def printing_parsing_news_in_json(content, number_of_news_to_show):
    # Convert news to json format and print them
    json_dict = {}
    newslist = []
    newsdict = {}

    for news in content.entries[:number_of_news_to_show]:
        for item in NEWS_PARTS:
            if item in news.keys():
                json_dict[item.capitalize()] = news[item]
        newslist.append(json_dict.copy())
    newsdict["news"] = newslist
    print(jsn.dumps(newsdict, indent=1))


def open_rss_link(source, limit, json, verbose):
    """
    Main function: receive link and params from bash, parse news and print them (and logs)
    :param source: link to take news
    :param limit: how many news tp return
    :param json: choose output format
    :param verbose: choose place to print logs
    :return: print news to stdout
    """
    logger = set_logger(verbose)

    # Receive link and start parsing
    try:
        content = feedparser.parse(source)
    except URLError as e:
        print("Bad link, please try again")

    logger.info(f"Starting reading link {source}")

    if limit or limit == 0:
        # Set how many news to print
        if limit <= 0:
            raise ValueError("Please insert haw many news you want to read (more than 0)")
        if limit <= len(content.entries):
            logger.info(f"Would read only {limit} number of news")
            number_of_news_to_show = limit
    else:
        number_of_news_to_show = len(content.entries)

    if json:
        logger.info(f"Convert news in json format")
        printing_parsing_news_in_json(content, number_of_news_to_show)
    else:
        printing_parsing_news(content, number_of_news_to_show)

    logger.info(f"End of reading")


def parse_command_line_arguments():
    # Parse arguments from command line
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader")
    parser.add_argument(
        "--version", action="version", version="Version 1.0.1", help="Print version info"
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
    arguments = parser.parse_args()
    return arguments


def main():
    # Call main function with parsed arguments
    arguments = parse_command_line_arguments()
    open_rss_link(arguments.source, arguments.limit, arguments.json, arguments.verbose)


if __name__ == "__main__":
    # Run the reader
    main()