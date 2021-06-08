""" Receive URL from the command line, read the data from it and print it to STDOUT """

import argparse
import sys
import requests
from bs4 import BeautifulSoup
import logging
import json

logging.basicConfig(level="INFO", format='%(levelname)s: %(message)s')
logger = logging.getLogger("rss_reader")


def get_args():
    """Return attributes parsed out of the command line"""
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

        if args.limit < 0:
            logger.error("--limit argument should take non-negative values. Enter the right value.")
            raise SystemExit

        return args

    except argparse.ArgumentError:
        logging.error("Catching an argumentError")
        sys.exit()


def get_response(url):
    """Get the server’s response from URL"""
    try:
        logging.info(f"Connecting to {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            logger.error(f"Failed to establish a new connection. Check the URL you have entered.")
            raise SystemExit
    except Exception as e:
        logger.error(f"Failed to establish a new connection. Exception message: {e}")
        raise SystemExit


def extract_data_from_xml(content, limit):
    """Parse limit news from xml and return a dictionary with news data"""
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
            images = []
            all_images = news.findAll("media:content")
            for image in all_images:
                image_link = image.get("url")
                images.append(image_link)
            news_item = {"Title": title, "Date": date, "Link": link, "Images": images}
            news_list.append(news_item)
        if news_list == []:
            logger.error("No content received. Check the RSS URL you have entered.")
            raise SystemExit
        else:
            data["News"] = news_list
        logger.info(f"Extracting {limit} news...")
    except Exception as e:
        logger.error(f"Parsing xml was failed. Check the RSS URL you have entered. {e}")
        raise SystemExit

    return data


def print_news(data):
    """Print news to STDOUT"""
    logger.info("Printing news...")
    print("\nFeed:", data["Feed"], "\n")
    for news_item in data["News"]:
        print("Title:", news_item["Title"])
        print("Date:", news_item["Date"])
        print("Link:", news_item["Link"])
        print("Images:", len(news_item["Images"]))
        print('\n'.join(news_item["Images"]), "\n")


def print_json(data):
    """Print news in JSON format to STDOUT and return JSON"""
    logger.info("Printing news in json format...")
    json_data = json.dumps(data, indent=3)
    print(json_data)
    return json_data


def main():
    """
    Get attributes parsed out of the command line.
    Turn off logging info if "--verbose" is not used.
    Get the server’s response from the received URL.
    Parse limit news from xml and return a dictionary with news data.
    Print news to STDOUT (in JSON format if "--json" is used).
    """
    try:
        args = get_args()

        if not args.verbose:
            logging.root.setLevel(40)

        logger.info("Got attributes from the command line.")

        content = get_response(args.rss_url)

        if content is not None:
            data = extract_data_from_xml(content.text, args.limit)
        else:
            logger.error(f"Parsing xml was failed. Check the RSS URL you have entered.")
            raise SystemExit

        if len(data):
            if args.json:
                print_json(data)
            else:
                print_news(data)
        else:
            logger.info(f"No data parsed from URL {args.rss_url}")
            raise SystemExit

        logger.info(f"Count of news: {len(data['News'])} \n")

    except Exception as e:
        logger.error(f"Exception message: {e}")


if __name__ == "__main__":
    main()
