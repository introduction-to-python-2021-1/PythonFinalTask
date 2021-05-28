import sys
import json
import argparse
import feedparser
import urllib.error
import logging.handlers

from reader.article import Article

__version__ = '1.3'


def parse_news(news, cursor, connection, url):
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

            store_news(news_list, cursor, connection, url)
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


def store_news(list_of_news, cursor, connection, url):
    """Storing news in a local storage"""
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


def execute_news(date, cursor, url):
    """Retrieving news for the selected date"""
    if url:
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


def check_url(source, cursor, connection):
    """Checking the validity of user-entered URL"""
    try:
        rss_news = feedparser.parse(source)
        result = parse_news(rss_news['entries'], cursor, connection, source)
    except urllib.error.URLError:
        raise SystemExit("Source isn't available")
    else:
        if len(result) == 0:
            raise SystemExit('Please, check if the entered link is correct!')
        else:
            return result


def create_arguments(argv):
    """Creates command line arguments"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', type=str, nargs='?', default=None, help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + __version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, nargs='?', default='', help='Sets the date the news will be displayed')
    parser.add_argument('--to_html', type=str, help='The path where new file will be saved')
    return parser


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
