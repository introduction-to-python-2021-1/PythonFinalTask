import requests
from bs4 import BeautifulSoup
import json
import argparse
import logging
import logging.handlers
import sys
from urllib.error import URLError


logging.basicConfig(level=logging.WARNING, format="%(message)s")
logger = None

def create_logger(verbose):
    """Creates a logger"""
    global logger
    if logger is None:
        logger = logging.getLogger()
    return logger


def command_arguments_parser(args):
    """ Adds positional and optional arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 1.0")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")
    args = parser.parse_args(args)
    return args


def parses_data(source, limit):
    """ Parses the data from the xml"""
    list_of_news = []
    dictionary = {}

    try:
        request = requests.get(source)
        if request.status_code == 200:
            soup = BeautifulSoup(request.content, 'xml')
            dictionary["Feed"] = soup.find("title").text
            news_for_print = soup.findAll("item", limit=limit)
            for news in news_for_print:
                title = news.find("title").text
                date = news.find("pubDate").text
                link = news.find("link").text
                images = []
                images_find = news.findAll("media:content")
                for image in images_find:
                    link_of_image = image.get("url")
                    images.append(link_of_image)
                # news_item = {"Title": title, "Date": date, "Link": link, "Description": description, "Images": images}
                news_item = {"Title": title, "Date": date, "Link": link, "Images": images}
                list_of_news.append(news_item)
            dictionary["News"] = list_of_news
    except Exception as e:
        print(f"Xml was failed: {e}")
    return dictionary

def rss_link(source, verbose):
    """Receive link with RSS news and try to parse it, print logs"""
    logger = create_logger(verbose)
    try:
        news_log = command_arguments_parser(source)
        if not source:
            raise ValueError
        logger.info(f"Reads link {source}")
    except URLError as e:
        logger.error(f"Error {e} in opening link {source}")
        return print("Change link and try again, please")
    except ValueError as e:
        logger.error(f"Error {e} in opening link {source}")
        return print("Add rss link, please")


def print_news(dictionary):
    """Print news on console"""
    print("\nFeed:", dictionary["Feed"], "\n")
    for news_item in dictionary["News"]:
        print("Title:", news_item["Title"])
        print("Date:", news_item["Date"])
        print("Link:", news_item["Link"])
        # print("Description:", news_item["Description"])
        print("Images:", len(news_item["Images"]))
        print('\n'.join(news_item["Images"]), "\n")
    print("Amount of news:", len(dictionary["News"]), "\n")


def print_json(dictionary):
    """Print json news on console"""
    print(json.dumps(dictionary, indent=3))
    with open("../json_format", "w") as file:
        json.dump(dictionary, file, indent=3)


def main():
    args = command_arguments_parser(sys.argv[1:])
    logger = create_logger(args.verbose)
    number_of_news = parses_data(args.source, args.limit)
    if args.limit:
        logger.info(f"Reads {args.limit} news' amount")
    if args.json:
        logger.info(f"In json")
        print_json(number_of_news)
    else:
        print_news(number_of_news)
    logger.info(f"The end")


if __name__ == "__main__":
    main()

