"""
Module contains functions to save news to html and pdf format by determinate html template.
Output files include number of news, limited by user.
Each news contains title, published date and link; and summary, description and one image (if they were in a source).
News takes from parsed news, saved to dictionary with news "newsdict".
"""

import os
import sys
import time

from jinja2 import Template
from xhtml2pdf import pisa


def make_html(newsdict: dict, one_news: dict):
    """ Make html file from all news from newsdict.

    :param newsdict: dictionary with parsed news "news"
    :param one_news: one news from newsdict
    :return: html file with all news, rendered by template
    """

    template = Template(
        open(os.path.join(os.getcwd(), "html_template.html")).read()
    )
    return template.render(newsdict=newsdict, one_news=one_news)


def save_html(user_path: str, newsdict: dict, number_of_news_to_show: int):
    """ Save news in html in a directory, chosen by user, in a volume (number of news), chosen by user.

    Name of the file include exact time of making file (joined on one string without spaces) to avoid rewritings.
    :param user_path: path to the file on users PC, chosen by him
    :param newsdict: dictionary with parsed news "news"
    :param number_of_news_to_show: limit number of news for saving
    :return: first write chosen number of news to html file, than return path to it
    """

    filename = "".join(str(time.time()))
    file_path = os.path.join(user_path, f"News from time {filename}.html")
    with open(file_path, "w", encoding="utf-8") as file:
        for one_news in newsdict["news"][:number_of_news_to_show]:
            file.write(make_html(newsdict, one_news))
    print(f"Your news was successfully save to '{file_path}' in html")
    return file_path


def save_pdf(user_path: str, newsdict: dict, number_of_news_to_show: int):
    """ Make html file with chosen number of news, create a pdf file in a chosen directory,write there converted html.

    Name of the file include exact time of making file (joined on one string without spaces) to avoid rewritings.
    :param user_path: path to the file on users PC, chosen by him
    :param newsdict: dictionary with parsed news "news"
    :param number_of_news_to_show: limit number of news for saving
    :return: False on success and True on errors
    """

    file_in_path = save_html(user_path, newsdict, number_of_news_to_show)
    filename = "".join(str(time.time()))
    file_out_path = os.path.join(user_path, f"News from time {filename}.pdf")
    with open(file_out_path, "w+b") as file_out, open(file_in_path, "r") as file_in:
        pisa_status = pisa.CreatePDF(src=file_in, dest=file_out)
        print(f"Your news was successfully save to '{file_out_path}' in pdf")
    os.remove(file_in_path)
    return pisa_status.err
