import os
import time

from jinja2 import Template


def make_html(newsdict, one_news):
    """
    Make html file from all news from newsdict
    :param newsdict: dictionary with parsed news "news"
    :param one_news: one news from newsdict
    :return: html file with all news, rendered by template
    """
    template = Template(
        open(os.path.join(os.getcwd(), "html_template.html")).read()
    )
    return template.render(newsdict=newsdict, one_news=one_news)


def save_html(user_path: str, newsdict: dict, number_of_news_to_show: int):
    """
    Save news in html in a directory, chosen by user, in a volume (number of news), chosen by user.
    Name of the file include exact time of making file (joined on one string without spaces) to avoid rewritings
    :param user_path: path to the file on users PC, chosen by him
    :param newsdict: dictionary with parsed news "news"
    :param number_of_news_to_show: limit number of news for saving
    :return: first write chosen number of news to html file, than return it
    """
    filename = "".join(str(time.time()))
    file_path = os.path.join(user_path, f"News from time {filename}.html")
    with open(file_path, "w") as file:
        for one_news in newsdict["news"][:number_of_news_to_show]:
            file.write(make_html(newsdict, one_news))
        return file
