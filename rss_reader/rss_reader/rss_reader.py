"""Main module. Receive input info from console, parse it and print result to stdout."""

import requests
from bs4 import BeautifulSoup
import json
import argparse
import logging
import logging.handlers
import sys
from urllib.error import URLError


def command_arguments_parser(args):
    """Adds positional and optional arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 1.2")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")
    args = parser.parse_args(args)
    return args


def create_logger(verbose):
    """Create the output for logs"""

    handlers = [logging.StreamHandler(sys.stdout)] if verbose else [logging.FileHandler("logs.log")]
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )
    logger = logging.getLogger()
    return logger


def server_answer(source):
    """Getting answer from server"""
    try:
        answer = requests.get(source)
        if answer.status_code == 404:
            print("Error 404. Please try to reload the page or check the link you entered")
            sys.exit()
        elif not source:
            print("Input url, please")
            sys.exit()
        elif answer.status_code == 200:
            print(f"Starting reading link {source}")
        return answer
    except URLError:
        print("Wrong link, try again, please")
        sys.exit()
    except ValueError:
        print("Insert rss link, please")
        sys.exit()


def parses_data(answer):
    """Parses data from the xml"""
    list_of_news = []
    data = {}

    try:
        buitiful_soup = BeautifulSoup(answer, "xml")
        data["feed"] = buitiful_soup.find("title").text
        news_for_print = buitiful_soup.findAll("item")
        for alone_news in news_for_print:
            title = alone_news.find("title").text
            pub_date = alone_news.find("pubDate").text
            link = alone_news.find("link").text
            images = []
            images_find = alone_news.findAll("media:content")
            for image in images_find:
                link_of_image = image.get("url")
                images.append(link_of_image)
            news_dictionary = {"title": title, "pubDate": pub_date, "link": link, "images": images}
            list_of_news.append(news_dictionary)
        data["news"] = list_of_news
    except Exception:
        print("Xml was failed")
    return data


def printing_news(data, limit):
    """Print news on console"""
    for num, part in enumerate(data["news"]):
        if num == limit:
            break
        print("title:", part["title"])
        print("pubDate:", part["pubDate"])
        print("link:", part["link"])
        print("images:", len(part["images"]))
        print('\n'.join(part["images"]), "\n")


def printing_json(data, limit):
    """Print json news on console"""
    data_json = data["news"][:limit]
    print(json.dumps(data_json, indent=3))


def main():
    args = command_arguments_parser(sys.argv[1:])
    answer = server_answer(args.source)
    logger = create_logger(args.verbose)

    if args.limit is not None:
        if args.limit <= 0:
            print("Invalid limit. Enter the limit (greater than 0), please")
            sys.exit()

    try:
        logger.info("Getting access to the RSS")
        number_of_news = parses_data(answer.text)
        if args.limit:
            logger.info(f"Reads amount of news - {args.limit}")
            print("Reads amount of news:", args.limit)
        if args.json:
            logger.info("In json")
            printing_json(number_of_news, args.limit)
        else:
            printing_news(number_of_news, args.limit)
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print("ConnectionError. Correct the URL, please")
    except requests.exceptions.MissingSchema:
        print("Incorrect URL. This is not the rss feed address")


if __name__ == "__main__":
    main()
