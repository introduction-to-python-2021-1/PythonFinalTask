"""Main module. Receive input info from console, parse it and print result to stdout."""
import requests
from bs4 import BeautifulSoup
import json
import argparse
import logging
import logging.handlers
import sys
import dateparser
import os
from datetime import datetime
from os import sep as os_sep
from xhtml2pdf import pisa


def command_arguments_parser(args):
    """Adds positional and optional arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 1.2")
    parser.add_argument("source", type=str, nargs="?", default=None,  help="RSS URL")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=str, help="Return news from date yyyymmdd from cash")
    parser.add_argument("--to_html", type=str, help="Convert news to html file. Path example 'd:/rss_news")
    parser.add_argument("--to_pdf", type=str, help="Convert news to html file. Path example 'd:/rss_news")
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
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print("ConnectionError or wrong link, try again, please")
        sys.exit()
    except requests.exceptions.MissingSchema:
        print("Incorrect URL. This is not the rss feed address")
        sys.exit()


def parses_data(answer, source):
    """Parses data from the xml"""
    list_of_news = []
    data = {}

    try:
        buitiful_soup = BeautifulSoup(answer, "xml")
        data["feed"] = buitiful_soup.find("title").text
        data["source"] = source
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
    limited_data_json = data["news"][:limit]
    data["news"] = limited_data_json
    print(json.dumps(limited_data_json, indent=3))


def compare_dates(date_of_publication, user_date_in_converted_format):
    """Compare date given by user(user_date_in_converted_format) and date from news(date_of_publication)"""
    converted_date_of_publication = dateparser.parse(date_of_publication, date_formats=["%y/%m/%d"])
    return converted_date_of_publication.date() == user_date_in_converted_format.date()


def news_cashing(data):
    """Save data in the file "cashed_news.txt" in json format"""
    file_for_cashing = os.path.join(os.getcwd(), "cashing_news.txt")
    with open(file_for_cashing, "a") as cash_file:
        cash_file.write(json.dumps(data))
        cash_file.write("\n")


def find_cashed_news(user_date_in_converted_format, source=None):
    """Checks the news data file"""
    cash_file = os.path.join(os.getcwd(), "cashing_news.txt")
    with open(cash_file, "r") as cash_file:
        list_of_news = []
        data_from_cash = {"source": "from cash file", "main_title": "Cashed news"}
        for json_dict in cash_file:
            data = json.loads(json_dict)

            if source and source != data["source"]:
                continue
            for num, part in enumerate(data["news"]):
                if compare_dates(part["pubDate"], user_date_in_converted_format):
                    list_of_news = [print("title:", part["title"]),
                                    print("pubDate:", part["pubDate"]),
                                    print("link:", part["link"]),
                                    print("images:", len(part["images"])),
                                    print('\n'.join(part["images"]), "\n")]
    if data:
        data_from_cash["news"] = list_of_news
        return data_from_cash
    else:
        raise AttributeError


def creating_cashing_news_data(user_date, source: str = None):
    """Receive user date from user, convert it into datetime and find cashed news"""
    user_date_in_converted_format = datetime.strptime(user_date, "%Y%m%d")
    if user_date_in_converted_format < datetime.strptime("20210601", "%Y%m%d"):
        print("Cashing news starts from June 1, 2021")
        sys.exit()
    data = find_cashed_news(user_date_in_converted_format, source)
    return data


def to_html(data, save_path, date):
    """Saving news in html format"""
    path = r"{0}rss_feed_time {1}.html".format(save_path + os_sep, date)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(path, "w", encoding="utf-8") as path_file:
        path_file.write('''
        <Html>
            <Head>
                <title>RSS reader feed</title>
            </Head>
            <Body>
        ''')
        for num, part in enumerate(data["news"]):
            path_file.write('''
                <h3>{}</h1>
                <a href = {}>Feed URL</a>
                <p>Date of publication: {}</p>
                <img src="{}" height="344" width="520" alt="Image can not be displaed">
                <hr>
                '''.format(part["title"], part["link"], part["pubDate"], part["images"]))
        path_file.write('''
            </Body>
        </Html>
        ''')
    print(f"The news file was created in path {path}")


def to_pdf(data, save_path, date):
    """Saving news in pdf format"""
    path = r"{0}rss_feed_time {1}.pdf".format(save_path + os_sep, date)
    img = False
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    try:
        answer = requests.get(data["source"])
        img = True
    except requests.exceptions.ConnectionError:
        pass
    pdf_news = '''<Html>
                        <Head>
                            <title>RSS reader feed</title>
                        </Head>
                    <Body>
                '''
    with open(path, "w+b") as path_file:
        for num, part in enumerate(data["news"]):
            pdf_news += '''
                <h3>{}</h1>
                <a href = {}>Feed URL</a>
                <p>Publication date: {}</p>
                {}
                <hr>
                '''.format(part["title"],
                           part["link"],
                           part["pubDate"],
                           f'<img src="{part["images"]}" height="344" width="520">' if img else "Image can not be "
                                                                                                "displaed")
        pdf_news += '''
            </Body>
        </Html>
        '''
        pisa.CreatePDF(pdf_news, dest=path_file)
    print(f"The news file was created in path {path}")


def main():
    args = command_arguments_parser(sys.argv[1:])
    logger = create_logger(args.verbose)

    if args.limit is not None:
        if args.limit <= 0:
            print("Invalid limit. Enter the limit (greater than 0), please")
            sys.exit()
    if args.date:
        try:
            data = creating_cashing_news_data(args.date, args.source)
        except (ValueError, TypeError, AttributeError, FileNotFoundError) as e:
            logger.error(f"{e} in parsing date '{args.date}'")
            print("Incorrect date (insert date like'20210601') or no news from this date or cashed news was not found.")
            sys.exit()

    else:
        try:
            logger.info("Getting access to the RSS")
            answer = server_answer(args.source)
            data = parses_data(answer.text, args.source)
            if args.limit:
                logger.info(f"Reads amount of news - {args.limit}")
            if args.json:
                printing_json(data, args.limit)
                news_cashing(data)
            else:
                printing_news(data, args.limit)
                news_cashing(data)
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.MissingSchema):
            return print()
    if args.to_html:
        to_html(data, args.to_html, datetime.now().strftime("%m.%d %H.%M.%S"))
    if args.to_pdf:
        to_pdf(data, args.to_pdf, datetime.now().strftime("%m.%d %H.%M.%S"))


if __name__ == "__main__":
    main()
