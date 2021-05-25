import json
import argparse
import feedparser
import urllib.error

from reader.article import Article


def parse_news(news, cursor, connection):
    """Creating list of news"""
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
        if source != source_title:
            source_title = source['title']

        image = default_value
        if media_content != image:
            image = media_content[0]['url']

        article = Article(title, link, published, source_title, description, image)
        news_list.append(article)

        store_news(news_list, cursor, connection)

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
        # return limit
    except ValueError:
        raise SystemExit('The argument "limit" should be a positive number')
    else:
        if limit < 1:
            raise SystemExit('The argument "limit" should be greater than 0')
        else:
            return limit


def store_news(list_of_news, cursor, connection):
    """Storing news in a local storage"""
    cursor.execute('''CREATE TABLE IF NOT EXISTS news
                   (title text, link text UNIQUE, full_date text, date text, source text, description text,
                   image text)''')
    list_of_values = []
    for item in list_of_news:
        try:
            new_date = item.date.strftime('%Y%m%d')
            new_article = [item.title, item.link, item.date, new_date, item.source, item.description, item.image]
            list_of_values.append(new_article)
            cursor.execute("INSERT OR REPLACE INTO news VALUES (?, ?, ?, ?, ?, ?, ?)", new_article)
        except AttributeError:
            print('zzzz')
    connection.commit()


def execute_news(date, cursor):
    """Retrieves news for the selected date"""
    cursor.execute('SELECT title, link, full_date, source, description, image FROM news WHERE date=:date',
                   {'date': date})
    articles = []
    for title, link, full_date, source, description, image in cursor.fetchall():
        articles.append(Article(title, link, full_date, source, description, image))
    return articles


# def check_URL(source, cursor, connection):
#     try:
#         rss_news = feedparser.parse(source)
#         result = parse_news(rss_news.entries, cursor, connection)
#         return result
#     except urllib.error.URLError:
#         print("Source isn't available")

def create_arguments(new_version):
    """Creates command line arguments"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + str(new_version), help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, nargs='?', default='', help='Sets the date the news will be displayed')

    args, unknown = parser.parse_known_args()
    return args
