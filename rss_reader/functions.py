import feedparser
import json

from rss_reader.article import Article


def read_rss(link, logger):
    """Creating list of news"""
    defaultValue = '---'

    def get_attribute(name):
        """Checking for the presence of a trasable attribute"""
        try:
            return entry[name]
        except KeyError:
            # logger.warning(f'There is no attribute "{name}" for selected article: "{entry.title}"')
            return defaultValue

    news_list = []

    rss_news = feedparser.parse(link)

    # news_list.append(rss_news.feed.title + '\n')

    for entry in rss_news.entries:
        title = get_attribute('title')
        link = get_attribute('link')
        published = get_attribute('published')
        source = get_attribute('source')
        description = get_attribute('description')
        media_content = get_attribute('media_content')

        sourceTitle = defaultValue
        if source != sourceTitle:
            sourceTitle = source['title']

        image = defaultValue
        if media_content != image:
            image = media_content[0]['url']

        article = Article(title, link, published, sourceTitle, description, image)
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
        print('The argument "limit" should be a positive number')
        raise SystemExit
