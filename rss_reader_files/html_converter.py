"""
This module provides funcs for converting feed to html format
"""

from rss_reader_files.templates import html_templates
import time


def convert_to_html(feed, path):
    """
    Convert feed to html format
    :param feed: feed object
    :param path: directory where news.html file will be saved
    """
    feed_items_html = []
    for item in feed.items:
        feed_item = html_templates.feed_item.render(title=item.title,
                                                    date=time.strftime("%y-%m-%d %H:%M", item.date),
                                                    content=item.content,
                                                    link=item.link,
                                                    links=item.links,
                                                    img=item.img,
                                                    )

        feed_items_html.append(feed_item)
    html_page = html_templates.feed.render(news=feed_items_html, title=feed.name)
    with open(path, 'w', encoding='utf-8') as html:
        html.write(html_page)
