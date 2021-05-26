import requests
from bs4 import BeautifulSoup
import json
import argparse
import logging
import logging.handlers
import sys


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


def answer_URL(source):
    """Answer to the input URL"""
    try:
        answer = requests.get(source)
        if answer.status_code == 200:
            return answer
    except Exception:
        print("Xml was failed. Input the correct URL, please")


def parses_data(data, limit):
    """ Parses data from the xml"""
    list_of_news = []
    dictionary = {}

    try:
        buitiful_soup = BeautifulSoup(data, 'xml')
        dictionary["Feed"] = buitiful_soup.find("title").text
        news_for_print = buitiful_soup.findAll("item", limit=limit)
        for alone_news in news_for_print:
            title = alone_news.find("title").text
            pub_date = alone_news.find("pubDate").text
            link = alone_news.find("link").text
            images = []
            images_find = alone_news.findAll("media:content")
            for image in images_find:
                link_of_image = image.get("url")
                images.append(link_of_image)
            news_dictionary = {"Title": title, "pubDate": pub_date, "Link": link, "Images": images}
            list_of_news.append(news_dictionary)
            dictionary["News"] = list_of_news
    except Exception:
        print("Xml was failed")
    return dictionary

def printing_news(dictionary):
    """Print news on console"""
    print("\nFeed:", dictionary["Feed"], "\n")
    for part in dictionary["News"]:
        print("Title:", part["Title"])
        print("pubDate:", part["pubDate"])
        print("Link:", part["Link"])
        print("Images:", len(part["Images"]))
        print('\n'.join(part["Images"]), "\n")
    print("Amount of news:", len(dictionary["News"]), "\n")


def printing_json(dictionary):
    """Print json news on console"""
    print(json.dumps(dictionary, indent=3))
    with open("json_format", "w") as json_file:
        json.dump(dictionary, json_file, indent=3)


def main():
    args = command_arguments_parser(sys.argv[1:])
    answer = answer_URL(args.source)
    if not answer:
        if args.verbose:
            print("No content received from URL", args.source)
        return False

    if args.limit == 0:
        print("Invalid limit. Enter the limit (greater than 0), please")
        sys.exit(0)

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    try:
        logging.info("Getting access to the RSS")
        number_of_news = parses_data(answer.text, args.limit)
        if args.limit:
            logging.info(f"Reads amount of news - {args.limit}")
        if args.json:
            logging.info("In json")
            printing_json(number_of_news)
        else:
            printing_news(number_of_news)
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print("ConnectionError. Correct the URL, please")

    except requests.exceptions.MissingSchema:
        print("Incorrect URL. Correct the URL, please")

if __name__ == "__main__":
 main()
