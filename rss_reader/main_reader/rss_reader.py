""" Main module. Receive input info from bash, parse it and print result to stdout. """
import argparse
import json as jsn
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from termcolor import colored
from urllib.error import URLError

import dateparser
import feedparser
from main_reader import add_colors
from main_reader import converter

NEWS_PARTS = ("title", "published", "summary", "description", "storyimage", "media_content", "link")


def set_logger(verbose: bool or None):
    """ Choose the output for logs and configure a logger.

    :param verbose: If True, prints logs not to the file, but to stdout
    :return: configured logger
    """

    handlers = [logging.StreamHandler(sys.stdout)] if verbose else [logging.FileHandler("logs.log")]
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )
    logger = logging.getLogger()
    return logger


def set_limit(len_news: int, limit: int or None):
    """ Set how many numbers of new to print.

    :param len_news: total number of news
    :param limit: user's parameter, that limit number of news to be printed;
    could be int or None (in case of None return value will be equal total number of news)
    :return: number of news to print or exit from the program, if limit <= 0
    """

    number_of_news_to_show = len_news
    if limit is not None:
        if limit <= 0:
            print("Please insert haw many news you want to read (more than 0)")
            sys.exit()
        elif limit <= len_news:
            number_of_news_to_show = limit
    return number_of_news_to_show


def make_news_dictionary(source: str, content) -> dict:
    """ Make a dictionary from FeedParserDict instance "content".

    :param source: link with rss news to save
    :param content: parsed link with rss news
    :return dictionary with parsed news "news", publication date "date" and source link "source"
    """

    innerdict = {}
    newslist = []
    newsdict = {"source": source, "main_title": content.feed.title}

    for news in content.entries:
        for item in NEWS_PARTS:
            if item in news:
                if item == "media_content" or item == "storyimage":
                    innerdict["Image"] = news[item][0]["url"]
                else:
                    innerdict[item.capitalize()] = news[item]
        newslist.append(innerdict.copy())
    newsdict["news"] = newslist

    return newsdict


def printing_parsing_news(newsdict: dict, number_of_news_to_show: int, colorize=None):
    """ Print parsed news to bash.

    :param number_of_news_to_show: limit number of news for parsing
    :param newsdict: dictionary with parsed news "news"
    :param colorize: if True, print news in colorized mode
    """

    if colorize:
        add_colors.print_roses(f"\nFeed: {newsdict['main_title']}")
        for one_news in newsdict["news"][:number_of_news_to_show]:
            add_colors.print_red_bold(f"\nTitle: {one_news['Title']}")
            add_colors.print_yellow_on_green(f"Date: {one_news['Published']}")
            add_colors.print_blue(f"Link: {one_news['Link']}")
            try:
                print(f"\nSummary: {one_news['Summary']}")
                print(f"\nDescription: {one_news['Description']}")
            except KeyError:
                pass
            add_colors.print_roses("\n\nLinks:")
            add_colors.print_blue(f"[1]: {one_news['Link']} (link)")
            try:
                add_colors.print_blue(f"[2]: {one_news['Image']} (image)\n")
            except KeyError:
                pass
    else:
        print(f"\nFeed: {newsdict['main_title']}")
        for one_news in newsdict["news"][:number_of_news_to_show]:
            print(f"\nTitle: {one_news['Title']}")
            print(f"Date: {one_news['Published']}")
            print(f"Link: {one_news['Link']}")
            try:
                print(f"\nSummary: {one_news['Summary']}")
                print(f"\nDescription: {one_news['Description']}")
            except KeyError:
                pass
            print("\n\nLinks:")
            print(f"[1]: {one_news['Link']} (link)")
            try:
                print(f"[2]: {one_news['Image']} (image)\n")
            except KeyError:
                pass


def printing_news_in_json(newsdict: dict, number_of_news_to_show: int, colorize=None):
    """ Limit number of news for printing, convert newsdict to json format and print it to bash.

    :param number_of_news_to_show: limit number of news for parsing
    :param newsdict: dictionary with parsed news "news"
    :param colorize: if True, print news in colorized mode
    """

    limited_news = newsdict["news"][:number_of_news_to_show]
    newsdict["news"] = limited_news
    text = jsn.dumps(newsdict, indent=1)

    if colorize:
        print(colored(text, "green", "on_yellow"))
    else:
        print(text)


def date_compare(dict_date: str, converted_user_date: datetime):
    """ Compare date given by user with datetime from a newsdict.

    :param dict_date: date from a newsdict
    :param converted_user_date:  date given by user
    :return: True if dates are equal, else False
    """

    converted_dict_date = dateparser.parse(dict_date, date_formats=["%y/%m/%d"])
    return converted_dict_date.date() == converted_user_date.date()


def write_cash(newsdict: dict):
    """ Write newsdict in the file "cashed_news.txt" in json format.

    :param newsdict: dictionary with parsed news "news"
    """

    cash_file_name = os.path.join(os.getcwd(), "cashed_news.txt")
    with open(cash_file_name, "a") as cash_file:
        cash_file.write(jsn.dumps(newsdict))
        cash_file.write("\n")


def find_cashed_news(converted_user_date: datetime, source=None):
    """ Check file with cashed news dictionaries.

    :param converted_user_date: date given by user
    :param source: source link given by user if any
    :return: newsdict_from_cash for reading news if there is suitable in cash, else raise AttributeError.
    If there were no cashed news before at all, means file with cashed news wasn't created, raise FileNotFoundError.
    """

    cash_file_name = os.path.join(os.getcwd(), "cashed_news.txt")
    with open(cash_file_name, "r") as cash_file:
        newslist = []
        newsdict_from_cash = {"source": "from cash file", "main_title": "Cashed news"}
        for json_dict in cash_file:
            newsdict = jsn.loads(json_dict)

            if source and source != newsdict["source"]:
                continue
            for one_news in newsdict["news"]:
                if date_compare(one_news["Published"], converted_user_date):
                    newslist.append(one_news)
    if newslist:
        newsdict_from_cash["news"] = newslist
        return newsdict_from_cash
    else:
        raise AttributeError


def open_rss_link(source: str, verbose: bool or None):
    """ Receive link with RSS news and try to parse it, print logs.

    :param source: link to take news
    :param verbose: choose place to print logs
    :return: parsed content from link. If no link, raise ValueError.
    """

    logger = set_logger(verbose)

    if not source:
        raise ValueError

    content = feedparser.parse(source)
    logger.info(f"Starting reading link {source}")

    return content


def making_cashed_news_dict(user_date: str, source: str = None):
    """ Receive user date in str format, convert it to datetime, call "find_cashed_news" to find suitable cashed news.

    :param user_date: date given by user in str format
    :param source: link to take news
    :return: newsdict for reading news if there is suitable in cash and number of news in it (len_news)
    If date is invalid and couldn't be converted in datetime, raise ValueError
    """

    converted_user_date = datetime.strptime(user_date, "%Y%m%d")
    if converted_user_date < datetime.strptime("20210501", "%Y%m%d"):
        print("Cashing news starts from May 1, 2021")
        sys.exit()

    newsdict = find_cashed_news(converted_user_date, source)
    len_news = len(newsdict["news"])
    return newsdict, len_news


def parse_command_line_arguments():
    """ Parse command line arguments.

    :return: parsed arguments
    """

    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader")
    parser.add_argument(
        "--version",
        action="version",
        version="Version 5.0.0",
        help="Print version info",
    )
    parser.add_argument("source", type=str, nargs="?", default=None, help="RSS URL")
    parser.add_argument(
        "--limit", type=int, help="Limit news topics if this parameter provided"
    )
    parser.add_argument(
        "--json", action="store_true", help="Print result as JSON in stdout"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Outputs verbose status messages"
    )
    parser.add_argument(
        "--colorize", action="store_true", help="Prints news to the console in colorized mode"
    )
    parser.add_argument(
        "--date", type=str, help="Return news from date yyyymmdd from cash"
    )
    parser.add_argument(
        "--to-pdf", type=str, help=r"Save news in pdf format in chosen path, eg 'E:\data' or '/home/user/data'"
    )
    parser.add_argument(
        "--to-html", type=str, help=r"Save news in html format in chosen path, eg 'E:\data' or '/home/user/data'"
    )
    arguments = parser.parse_args()
    return arguments


def main():
    """
    Receive parsed arguments, call functions to set logger and number of news to show, choose format
    for of news to print (json or not) and call valid function fpr printing, print logs.
    """

    arguments = parse_command_line_arguments()

    logger = set_logger(arguments.verbose)

    if arguments.date:
        try:
            newsdict, len_news = making_cashed_news_dict(arguments.date, arguments.source)
            logger.info(f"News will be reading from cash")
        except (ValueError, TypeError) as e:
            logger.error(f"{e} was appearing with parsing date '{arguments.date}'")
            print("Invalid date, please insert date like '20210715'.")
            sys.exit()
        except AttributeError as e:
            logger.error(f"{e} was appearing with parsing date '{arguments.date}'")
            print("No news from this date")
            sys.exit()
        except FileNotFoundError as e:
            logger.error(f"{e} was appearing with parsing date '{arguments.date}'")
            print("There are no cashed news, "
                  "please read some news from external sources before trying to access cash")
            sys.exit()
    else:
        try:
            content = open_rss_link(arguments.source, arguments.verbose)
        except URLError as e:
            logger.error(f"Error {e} raised with trying to open link {arguments.source}")
            print("Bad link, please try again")
            sys.exit()
        except ValueError as e:
            logger.error(f"Error {e} raised with trying to open link {arguments.source}")
            print("Please insert rss link")
            sys.exit()
        len_news = len(content.entries)
        newsdict = make_news_dictionary(arguments.source, content)
        write_cash(newsdict)

    if arguments.limit:
        logger.info(f"Would read only {arguments.limit} number of news")

    number_of_news_to_show = set_limit(len_news, arguments.limit)

    if arguments.json:
        logger.info(f"Convert news in json format")
        printing_news_in_json(newsdict, number_of_news_to_show, arguments.colorize)
    else:
        printing_parsing_news(newsdict, number_of_news_to_show, arguments.colorize)

    if arguments.to_html:
        logger.info(f"News will be saved in html on path {arguments.to_html}")
        try:
            converter.save_html(arguments.to_html, newsdict, number_of_news_to_show)
        except FileNotFoundError as e:
            logger.error(f"{e} was appearing with the way '{arguments.to_html}'")
            print("Please write a valid existing absolute path to a destination directory, "
                  "filename will be generated automatically")
            sys.exit()
    elif arguments.to_pdf:
        logger.info(f"News will be saved in pdf on path {arguments.to_pdf}")
        try:
            converter.save_pdf(arguments.to_pdf, newsdict, number_of_news_to_show)
            logger.info(f"Temporary html file was removed from '{arguments.to_pdf}'")
        except TypeError as e:
            logger.error(f"{e} was appearing with the way '{arguments.to_pdf}'")
            sys.exit()
        except FileNotFoundError as e:
            logger.error(f"{e} was appearing with the way '{arguments.to_pdf}'")
            print("Please write a valid existing absolute path to a destination directory, "
                  "filename will be generated automatically")
            sys.exit()

    logger.info(f"End of reading")


if __name__ == "__main__":
    main()
