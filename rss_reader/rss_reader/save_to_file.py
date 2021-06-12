# Author: Julia Los <los.julia.v@gmail.com>.

"""Python command-line RSS reader

This module contains functions for save the utility's result to file.
"""

import jinja2
import os
import xml.etree.ElementTree as et

from datetime import datetime

_html_template = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
  </head>
  <body>
    <h1 align="center">{{ title }}</h1>
    {% for channel in data %}
    <div id={{ channel.channel_id }}>
      <h2 align="center">{{ channel.channel_title }}</h2>
      {% if channel.news %}
      {%- for item in channel.news %}
      <div>
        <h3>News № {{ item.number }}</h3>
        <p><b>Title:</b> {{ item.title }}</p>
        <p><b>Link:</b> <a href={{ item.link }}>{{ item.link }}</a></p>
        {% if item.author %}
        <p><b>Author:</b> {{ item.author }}</p>
        {%- endif %}
        {% if item.date %}
        <p><b>Date:</b> {{ item.date }}</p>
        {%- endif %}
        {% if item.image %}
        <img src={{ item.image }} width="600" height="400">
        {%- endif %}
        {% if item.description %}
        <p>{{ item.description }}</p>
        {%- endif %}
      </div>
      {% endfor %}
      {% endif %}
    </div>
    {% endfor %}
  </body>
</html>"""


def check_filename(filename, extent):
    """Check if the filename is correct."""
    if not filename or filename == '':
        return

    root, ext = os.path.splitext(filename)

    if ext == '':
        if os.path.basename(filename) == '':
            return

        return filename + extent
    else:
        if ext != extent:
            return

        return filename


def save_to_fb2(filename, data, logger=None):
    """Save data to file in fb2 format."""
    if logger:
        logger.info("Save data to file in fb2 format...")

    filename = check_filename(filename, '.fb2')

    if filename is None:
        if logger:
            logger.warning("Filename is incorrect.")
        return

    if data is None:
        if logger:
            logger.warning("Data is None.")
        return

    if len(data) == 0:
        if logger:
            logger.warning("Data is empty.")
        return

    xml_root = et.Element('FictionBook', {'xmlns': "http://www.gribuser.ru/xml/fictionbook/2.0",
                                          'xmlns:l': "http://www.w3.org/1999/xlink"})
    # description
    xml_description = et.SubElement(xml_root, 'description')
    # description - title info
    xml_title_info = et.SubElement(xml_description, 'title-info')
    et.SubElement(xml_title_info, 'genre').text = 'comp_soft'
    xml_author = et.SubElement(xml_title_info, 'author')
    et.SubElement(xml_author, 'nickname').text = 'RSSReader'
    et.SubElement(xml_author, 'email').text = 'RSSReader@gmail.com'
    et.SubElement(xml_title_info, 'book-title').text = 'RSS Reader utility results'
    xml_annotation = et.SubElement(xml_title_info, 'annotation')
    xml_p = et.SubElement(xml_annotation, 'p')
    xml_p.text = 'News found by RSS Reader utility.'
    day_create = datetime.today()
    xml_date = et.SubElement(xml_title_info, 'date', {'value': day_create.strftime("%Y-%m-%d")})
    xml_date.text = day_create.strftime("%d %B, %Y")
    et.SubElement(xml_title_info, 'lang').text = 'en'
    # description - document info
    xml_document_info = et.SubElement(xml_description, 'document-info')
    xml_author = et.SubElement(xml_document_info, 'author')
    et.SubElement(xml_author, 'first-name').text = 'Larina'
    et.SubElement(xml_author, 'last-name').text = 'Fox'
    et.SubElement(xml_author, 'email').text = 'LarinaFox@gmail.com'
    et.SubElement(xml_document_info, 'program-used').text = 'RSSReader 4.0'
    et.SubElement(xml_document_info, 'date', {'value': '2021-05-29'}).text = '29 May, 2021'
    et.SubElement(xml_document_info, 'id').text = '2021_05_29_18_00_00'
    et.SubElement(xml_document_info, 'version').text = '1.0'
    xml_history = et.SubElement(xml_document_info, 'history')
    et.SubElement(xml_history, 'p').text = '1.0 - preparation fb2'
    # body
    xml_body = et.SubElement(xml_root, 'body')
    xml_title = et.SubElement(xml_body, 'title')
    et.SubElement(xml_title, 'p').text = 'RSS Reader utility results'
    xml_main_section = et.SubElement(xml_body, 'section')

    for channel in data:
        xml_channel = et.SubElement(xml_main_section, 'section', {'id': channel.get('channel_id', '')})
        et.SubElement(xml_channel, 'title').text = channel.get('channel_title', '')

        if channel.get('news') is None:
            continue

        for item in channel['news']:
            xml_news = et.SubElement(xml_channel, 'section')
            et.SubElement(xml_news, 'p').text = f"News № {item.get('number', '')}"
            et.SubElement(xml_news, 'p').text = f"Title: {item.get('title', '')}"
            xml_news_link = et.SubElement(xml_news, 'p')
            xml_news_link.text = 'Link: '
            xml_news_link_a = et.SubElement(xml_news_link, 'a', {'l:href': item.get('link', '')})
            xml_news_link_a.text = item.get('link', '')

            if item.get('author', '') != '':
                et.SubElement(xml_news, 'p').text = f"Author: {item['author']}"

            if item.get('date', '') != '':
                et.SubElement(xml_news, 'p').text = f"Date: {item['date']}"

            if item.get('image', '') != '':
                et.SubElement(xml_news, 'image', {'l:href': item.get('image', '')})

            if item.get('description', '') != '':
                et.SubElement(xml_news, 'p').text = f"\n{item['description']}"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            xml_tree = et.ElementTree(xml_root)
            et.indent(xml_tree)
            xml_tree.write(f, encoding="unicode", xml_declaration=True)
            print(f"Loaded news save to file: {f.name}.")
    except OSError:
        if logger:
            logger.error('Failed to save data to fb2 file.')


def save_to_html(filename, data, logger=None):
    """Save data to file in html format."""
    if logger:
        logger.info("Save data to file in html format...")

    filename = check_filename(filename, '.html')

    if filename is None:
        if logger:
            logger.warning("Filename is incorrect.")
        return

    if data is None:
        if logger:
            logger.warning("Data is None.")
        return

    if len(data) == 0:
        if logger:
            logger.warning("Data is empty.")
        return

    environment = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
    template = environment.from_string(_html_template)
    html_text = template.render(title="RSS Reader utility results", data=data)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_text)
            print(f"Loaded news save to file: {f.name}.")
    except OSError:
        if logger:
            logger.error('Failed to save data to html file.')
