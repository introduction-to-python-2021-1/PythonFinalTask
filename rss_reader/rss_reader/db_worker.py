from peewee import Model, SqliteDatabase, CharField, DateField
from os import sep as os_sep
import pathlib


def get_path(file_name='rss_data_storage.db'):
    return str(pathlib.Path(__file__).parent.absolute()) + os_sep + file_name


db = SqliteDatabase(get_path(), autoconnect=False)


class RssStorage(Model):
    title = CharField(max_length=180, primary_key=True, null=False, unique=True)
    pubDate = DateField()
    link = CharField(max_length=250, null=False)
    media = CharField(max_length=250, null=True)

    class Meta:
        database = db
