"""
rss_reader.py - receives URL from the command line and read the data from it and output it in STDOUT
"""

import argparse
import requests
from bs4 import BeautifulSoup
import json


# URL = "https://www.theguardian.com/world/rss"


def get_args():
    """inspects the command line and builds a Namespace object from attributes parsed out of the command line"""
    try:
        parser = argparse.ArgumentParser(
            description='RSS reader - a command-line utility which receives URL '
                        'and prints results in human-readable format'
        )

        parser.add_argument('rss_url', help="RSS url to parse")
        parser.add_argument('--version', action="version", help="Print version info", version='Version 0.2')
        parser.add_argument('--json', help="Print result as JSON in stdout", action="store_true")
        parser.add_argument('-v', '--verbose', action="store_true", help="Outputs verbose status messages")
        parser.add_argument('--limit', type=int, help="Limit news topics if this parameter provided", default=0)

        args = parser.parse_args()
        print(args)
        return args

    except argparse.ArgumentError:
        print("Catching an argumentError")


def verbose_args(args):
    """prints arguments info"""

    print("Verbosity is turned on.")
    print("Program runs with the given argument's values:")
    print(f"rss_url = {args.rss_url}, json = {args.json}, verbose = {args.verbose}, limit = {args.limit}")


def get_response(url):
    """tries to get the server’s response"""
    try:
        response = requests.get(url)
        # if args.verbose:
        #     print(f"Getting xml HTTP response: {response.status_code}")
        if response.status_code == 200:
            print(type(response))
            return response
    except Exception as e:
        print(f"Failed to establish a new connection. Check the URL you have entered.")


def extract_xml(content, limit):
    """parses data from xml"""
    news_list = []
    data = {}
    try:
        soup = BeautifulSoup(content, 'xml')
        data["Feed"] = soup.find("title").text
        all_news = soup.findAll("item", limit=limit)
        for news in all_news:
            title = news.find("title").text
            date = news.find("pubDate").text
            link = news.find("link").text
            # description = news.find("description").text
            images = []
            all_images = news.findAll("media:content")
            for image in all_images:
                image_link = image.get("url")
                images.append(image_link)
            # news_item = {"Title": title, "Date": date, "Link": link, "Description": description, "Images": images}
            news_item = {"Title": title, "Date": date, "Link": link, "Images": images}
            news_list.append(news_item)
        data["News"] = news_list
    except Exception as e:
        print(f"Getting xml was failed: {e}")

    return data


def print_news(data):
    """prints data in special format into STDOUT"""
    print("\nFeed:", data["Feed"], "\n")
    for news_item in data["News"]:
        print("Title:", news_item["Title"])
        print("Date:", news_item["Date"])
        print("Link:", news_item["Link"])
        # print("Description:", news_item["Description"])
        print("Images:", len(news_item["Images"]))
        print('\n'.join(news_item["Images"]), "\n")
    print("Count of news:", len(data["News"]), "\n")


def print_json(data):
    """prints data in JSON format into STDOUT"""
    json_data = json.dumps(data, indent=3)
    print(json_data)
    return json_data
    # with open("json_format", "w") as file: #??? ../
    #     json.dump(data, file, indent=3)


def main():
    try:
        args = get_args()
        if args.verbose:
            verbose_args(args)

        content = get_response(args.rss_url)
        if not content:
            if args.verbose:
                print("No content received from URL", args.rss_url)
            return False

        data = extract_xml(content.text, args.limit)

        if len(data):
            if args.json:
                print_json(data)
            else:
                print_news(data)
        else:
            if args.verbose:
                print("No data parsed from URL", args.rss_url)
    except Exception as e:
        print(f"Exception message: {e}")


if __name__ == "__main__":
    main()
