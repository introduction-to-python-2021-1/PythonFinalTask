import json

from rss_reader.article import Article


def parse_news(news):
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

    return news_list


def make_json(result):
    """Converting news in json format"""
    new_result = result.to_dict()
    json_result = json.dumps(new_result)
    return json_result


def check_limit(limit_value):
    """Checking the validity of user-entered limit"""
    try:
        limit = int(limit_value)
        return limit
    except ValueError:
        raise SystemExit(ValueError, 'The argument "limit" should be a positive number')
