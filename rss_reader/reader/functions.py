import json

from reader.article import Article


def parse_news(news, cursor, connection):
    """Creating list of news"""
    default_value = '---'

    def get_attribute(name):
        """Checking for the presence of a trasable attribute"""
        try:
            return entry[name]
        except KeyError:
            return default_value

    news_list = []
    for entry in news:
        title = get_attribute('title')
        link = get_attribute('link')
        published = get_attribute('published')
        source = get_attribute('source')
        description = get_attribute('description')
        media_content = get_attribute('media_content')

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
    json_result = json.dumps(new_result, sort_keys=True, indent=4)
    return json_result


def check_limit(limit_value):
    """Checking the validity of user-entered limit"""
    try:
        limit = int(limit_value)
        return limit
    except ValueError:
        raise SystemExit(ValueError, 'The argument "limit" should be a positive number')


def store_news(list_of_news, cursor, connection):
    """Storing news in a local storage"""
    cursor.execute('''CREATE TABLE IF NOT EXISTS news
                   (title text, link text UNIQUE, full_date text, date text, source text, description text,
                   image text)''')
    list_of_values = []
    for item in list_of_news:
        new_date = item.date.strftime('%Y%m%d')
        new_article = [item.title, item.link, item.date, new_date, item.source, item.description, item.image]
        list_of_values.append(new_article)
        cursor.execute("INSERT OR REPLACE INTO news VALUES (?, ?, ?, ?, ?, ?, ?)", new_article)
    connection.commit()


def execute_news(date, cursor):
    """Retrieves news for the selected date"""
    cursor.execute('SELECT title, link, full_date, source, description, image FROM news WHERE date=:date',
                   {'date': date})
    articles = []
    for title, link, full_date, source, description, image in cursor.fetchall():
        articles.append(Article(title, link, full_date, source, description, image))
    return articles
