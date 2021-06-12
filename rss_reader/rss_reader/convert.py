import os
import logging

import pandas as pd
from ebooklib import epub


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


class Epub:
    def __init__(self):
        self.book = epub.EpubBook()
        self.book.set_identifier('rss news')
        self.book.add_author("Remnev Aleksandr")
        self.book.set_language('en')

    def create_book(self, feed):
        """
        add news on epub format
        :param feed: feed news
        :return: book of news
        """
        logging.debug("Starting format html for epub file")
        self.book.spine = ['nav']
        self.book.toc = []
        for title, date, link, img in zip(feed["Title"], feed["Date"], feed['Link'], feed["img"]):
            chapter = epub.EpubHtml(title=title, file_name=title + '.xhtml')
            content = f"<h4>{title}</h4><br>Date:{date}<br><a href='{link}'>Link<br><img src='{img}'" \
                      f"alt='NoPhoto' ></a>"
            chapter.set_content(str(content))
            self.book.add_item(chapter)
            self.book.toc.append(chapter)

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        self.book.add_item(nav_css)
        logging.debug("Structure for epub file created")
        return self.book

    def make_file(self, feed, path):
        """
        Create file on epub format
        :param feed: feed of news to save in file
        :param path: path to the file on pc
        """
        data = self.create_book(feed)
        file = "".join(str("book of news"))
        file_path = os.path.join(path, f"{file}.epub")
        epub.write_epub(f"{file_path}", data, {})
        if not os.path.exists(file_path):
            logger.error(f"Bad path")


class HTML:
    def __init__(self, feed):
        self.html = pd.DataFrame(feed)

    def prepare(self):
        """Make a valid ling and img"""
        for i, link in enumerate(zip(self.html["Link"], self.html["img"])):

            self.html["Link"][i] = f"<a href='{link[0]}'>Link </a>"
            self.html['img'][i] = f"<a href=''><img src='{link[1]}' width='400' alt='NoPhoto'></a>"

    def make_file(self, path):
        """
            Create HTML file format
            :param path: path to the file on pc
        """
        self.prepare()
        file_ = "".join(str("News"))
        file_path = os.path.join(path, f"{file_}.html")
        self.html = self.html.to_html(escape=False)
        with open(f"{file_path}", "w", encoding="utf-8") as file:
            file.write(self.html)
