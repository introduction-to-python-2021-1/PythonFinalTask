"""
    Module contains class for convenient work with db
"""
import sqlite3

from utils import util


class DbProcessor:
    """
    Class for working with db
    """

    def __init__(self, db_name):
        self.dbi = self.create_connection(db_name=db_name)

    def _dict_factory(self, cursor, row):
        """
        Method for setting row_factory to get data
        fom base in convenient view
        :param cursor: db cursor
        :param row: selected row
        :return: dict with selected row elements
        """
        output_dict = {}
        for index, column in enumerate(cursor.description):
            output_dict[column[0]] = row[index]
        return output_dict

    def create_connection(self, db_name: str):
        """
        Method for creating connection to db
        :param db_name: name of sqlite db to be connected
        :return: connection to db
        """
        util.create_directory(db_name)
        dbi = sqlite3.connect(db_name)
        dbi.row_factory = self._dict_factory
        return dbi

    def perform_query(self, query: str = ""):
        """
        Perform user query and commit changes into db
        :param query: query to be performed
        :return: None
        """
        cursor = self.dbi.cursor()
        cursor.execute(query)
        self.dbi.commit()

    def select(self, select_query: str = ""):
        """
        Perform user SELECT query
        return: array of dict with select results
        :param select_query: query to be performed
        :return: None
        """
        cursor = self.dbi.cursor()
        cursor.execute(select_query)
        select_res = cursor.fetchall()
        return select_res

    def insert(self, table_name: str, insert_values: dict, ignore: bool = False):
        columns = ','.join(insert_values.keys())
        values = ','.join('?' * len(insert_values))
        ignore_word = "OR IGNORE" if ignore else ""
        query = f"INSERT {ignore_word} INTO {table_name} ({columns}) VALUES ({values})"
        self.dbi.execute(query, tuple(insert_values.values()))
        self.dbi.commit()

    def close_connection(self):
        self.dbi.close()