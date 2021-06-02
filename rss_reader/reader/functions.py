import sys
import json
import argparse
import feedparser
import urllib.error
import logging.handlers
import datetime
import os
from dominate import tags
from pathlib import Path
from xhtml2pdf import pisa

from reader.article import Article

__version__ = '1.4'


def parse_news(news):
    """Creating list of news"""
    try:
        default_value = '---'

        news_list = []
        for entry in news:
            title = entry.get('title', default_value)
            link = entry.get('link', default_value)
            published = entry.get('published', default_value)
            source = entry.get('source', default_value)
            description = entry.get('description', default_value)
            media_content = entry.get('media_content', default_value)

            source_title = default_value
            if source != default_value:
                source_title = source['title']

            image = default_value
            if media_content != image:
                image = media_content[0]['url']

            article = Article(title, link, published, source_title, description, image)
            news_list.append(article)

    except AttributeError:
        raise SystemExit('Sorry, no news to parse!')

    return news_list


def make_json(result):
    """Converting news in json format"""
    new_result = result.to_dict()
    json_result = json.dumps(new_result, indent=4)
    return json_result


def check_limit(limit_value):
    """Checking the validity of user-entered limit"""
    try:
        limit = int(limit_value)
    except ValueError:
        raise SystemExit('The argument "limit" should be a positive number')
    else:
        if limit < 1:
            raise SystemExit('The argument "limit" should be greater than 0')
        else:
            return limit


def store_news(list_of_news, connection, url):
    """Storing news in a local storage"""
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS news
                   (title text, link text UNIQUE, full_date text, date text, source text, description text,
                   image text, url text)''')
    list_of_values = []
    for item in list_of_news:
        new_date = item.date.strftime('%Y%m%d')
        new_article = [item.title, item.link, item.date, new_date, item.source, item.description, item.image]
        list_of_values.append(new_article)

        sql = "INSERT OR REPLACE INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, (new_article[0], new_article[1], new_article[2], new_article[3], new_article[4],
                             new_article[5], new_article[6], url))
    connection.commit()


def execute_news(date, connection, url, logger):
    """Retrieving news for the selected date"""
    cursor = connection.cursor()
    if url:
        logger.info(f"Retrieves news from the selected url ({url})...")
        cursor.execute('SELECT title, link, full_date, source, description, image, url FROM news WHERE date=:date '
                       'and url=:url', {'date': date, 'url': url})
    else:
        cursor.execute('SELECT title, link, full_date, source, description, image, url FROM news WHERE date=:date',
                       {'date': date})
    records = cursor.fetchall()
    articles = []
    for title, link, full_date, source, description, image, url in records:
        articles.append(Article(title, link, full_date, source, description, image))
    return articles


def get_from_url(source):
    """Parses the received data from user-entered URL"""
    try:
        rss_news = feedparser.parse(source)
        result = parse_news(rss_news['entries'])
    except urllib.error.URLError:
        raise SystemExit("Source isn't available")
    else:
        if len(result) == 0:
            raise SystemExit('Please, check if the entered link is correct!')
        else:
            return result


def get_from_db(date, source, connection, logger):
    """Get data from DB by url and date"""
    try:
        args_date = (datetime.datetime.strptime(date, '%Y%m%d')).date()
        result = execute_news(date, connection, source, logger)
        if len(result) == 0:
            raise SystemExit(f"Sorry, there are no articles for {args_date}!")
        else:
            return result
    except ValueError:
        raise SystemExit('Please, enter the date in the following format: "YYYYMMDD".')


def create_arguments(argv):
    """Creates command line arguments"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', type=str, nargs='?', default=None, help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + __version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, nargs='?', default='', help='Sets the date the news will be displayed')
    parser.add_argument('--to-html', type=Path, help='The absolute path where new .html file will be saved')
    parser.add_argument('--to-pdf', type=Path, help='The absolute path where new .pdf file will be saved')
    args = parser.parse_args(argv[1:])
    return vars(args)


def create_logger():
    """Creating logger"""
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler('../../../logs.txt')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.disable()
    return logger


def check_path_to_directory(path_to_directory, logger):
    """Checks if the path to the folder exists"""
    logger.info('Checking the entered path...')
    if os.path.isdir(path_to_directory) is False:
        logger.error('Entered path is invalid: not a folder')
        raise NotADirectoryError('Entered path is invalid: folder does not exist')
    else:
        return True


def html_factory(article, html_file):
    """Represents Article object in html-format"""
    with html_file:
        tags.h1(article.title)
        tags.p(tags.b('Title: '), article.title)
        tags.p(tags.b('Link: ', tags.a(tags.b(article.link), href=article.link, )))
        tags.p(tags.b('Date: '), article.date.strftime("%a, %d %B, %Y"))
        tags.p(tags.b('Source: '), article.source)
        tags.p(tags.b('Description: '), article.description)
        if article.image != '---':
            tags.p(tags.img(style="width:360px", src=article.image))
        else:
            tags.p(tags.b('Sorry, no images for this article'))
    return html_file


def save_news_in_html_file(news, path_to_html, logger):
    """Creates html-file and saves news in it"""
    check_path_to_directory(path_to_html, logger)
    html_file = tags.html(title='RSS news')
    html_file.add(tags.head(tags.meta(charset='utf-8')))

    logger.info('Converting news to html format...')
    for article in news:
        html_factory(article, html_file)

    path = os.path.join(path_to_html, 'rss_news.html')
    logger.info('Creating html-file...')
    with open(path, 'w', encoding='utf-8') as file_html:
        file_html.write(str(html_file))
    logger.info('Html-file is created successfully!')
    return file_html


def save_news_in_pdf_file(news, path_to_pdf, logger, html_args=None):
    """Represents articles in pdf-format"""
    html_file = save_news_in_html_file(news, path_to_pdf, logger)
    path = os.path.join(path_to_pdf, 'rss_news.pdf')
    try:
        with open(path, 'wb') as pdf_file, open(html_file.name, 'r', encoding='utf-8') as html_file:
            logger.info('Creating pdf-file...')
            pisa.CreatePDF(src=html_file, dest=pdf_file)
            logger.info("Pdf-file is created successfully!")
            if html_args is None:
                html_file.close()
                os.remove(html_file.name)
                logger.info("Temporary html-file was deleted")
            return pdf_file
    except FileNotFoundError:
        raise SystemExit('Please, check the existing of file')
