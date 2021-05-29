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
    parser.add_argument("--date", type=str)
    args = parser.parse_args(args)
    return args


def server_answer(source):
    """Getting answer from server"""

    try:
        answer = requests.get(source)
        if not source:
            print("Input the url, please")
        elif answer.status_code == 200:
            return answer
        elif answer.status_code == 403:
            print("Error 403. Forbidden. Access denied")
        elif answer.status_code == 404:
            print("Error 404. Please try to reload the page")
        else:
            print("Input the correct URL, please")
    except URLError as e:
        print(f"Error {e} in opening the link {source}")


def parses_data(answer):
    """Parses data from the xml"""
    list_of_news = []
    data = {}

    try:
        buitiful_soup = BeautifulSoup(answer.content, "xml")
        data["feed"] = buitiful_soup.find("title").text
        all_news = buitiful_soup.findAll("item")
        for alone_news in all_news:
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
        print("Amount of news:", len(data["news"]), "\n")


def printing_json(data, limit):
    """Print json news on console"""
    for num, part in enumerate(data["news"]):
        if num == limit:
            break
    print(json.dumps(data, indent=3))


def main():
    args = command_arguments_parser(sys.argv[1:])
    answer = server_answer(args.source)

    try:
        if args.limit is not None:
            if args.limit <= 0:
                print("Invalid limit. Enter the limit (greater than 0), please")
                sys.exit()
    except TypeError:
        pass

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    try:
        logging.info("Getting access to the RSS")
        data = parses_data(answer)

        if args.limit:
            logging.info(f"Reads amount of news - {args.limit}")

        if args.json:
            logging.info("In json")
            printing_json(data, args.limit)

        else:
            printing_news(data, args.limit)

    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print("ConnectionError. Correct the URL, please")
        sys.exit(0)

    except requests.exceptions.MissingSchema:
        print("Incorrect URL. This is not the rss feed address")


if __name__ == "__main__":
    main()