import os
import sqlite3

from rss_reader.constants import PROJECT_ROOT


class DB:
    def __init__(self):
        self.path_to_db = os.path.join(PROJECT_ROOT, "news.db")

    @property
    def connection(self):
        """Return connection to db"""
        connection = sqlite3.connect(self.path_to_db)
        connection.row_factory = sqlite3.Row
        return connection

    def execute(self, query: str, connection, parameters: tuple = (), fetchone=False, fetchall=False, commit=False):
        cursor = connection.cursor()
        try:
            cursor.execute(query, parameters)
            data = None
            if commit:
                connection.commit()
            if fetchone:
                data = cursor.fetchone()
            elif fetchall:
                data = [dict(row) for row in cursor.fetchall()]
            return data
        finally:
            connection.close()

    def create_schema(self):
        query = """
            CREATE TABLE IF NOT EXISTS News(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rss_source TEXT NOT NULL,
            pubdate TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT UNIQUE,
            image_url TEXT NOT NULL
            )
        """
        self.execute(query, self.connection, commit=True)

    def add_news(self, news):
        """
            Add news to the database.
                Parameters:
                    news: tuple with news parameters(rss_source, pubdate, title, image(url), link)
        """
        query = "INSERT INTO News(rss_source, pubdate, title, image_url, link) VALUES(?, ?, ?, ?, ?)"
        self.execute(query, self.connection, news, commit=True)

    def select_news_from_cache(self, rss_source=None, pubdate=None):
        """
            Select news by pubdate and rss_source.
                Parameters:
                    pubdate=Date (YYYY-MM-DD format)
                    rss_source: optional, string with URL of rss-feed
                Return list of dicts with news parameters(pubdate, title, link, image(url))
        """
        if not rss_source:
            query = "SELECT rss_source, pubdate, title, image_url, link FROM News WHERE pubdate = ?"
            parameters = (pubdate,)
        else:
            query = "SELECT pubdate, title, image_url, link FROM News WHERE rss_source = ? AND pubdate = ?"
            parameters = (rss_source, pubdate,)
        return self.execute(query, self.connection, parameters, fetchall=True)
