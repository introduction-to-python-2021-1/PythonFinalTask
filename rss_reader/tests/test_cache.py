from os import remove
from os.path import join
from unittest import TestCase

from rootpath import detect

from modules.cache import Cache
from rss_reader.rss_reader.rss_reader import create_logger
from tests.data.news_list import news


class TestCache(TestCase):
    def setUp(self) -> None:
        logger = create_logger()
        self.cache = Cache(logger=logger, file_name='test_cache.json')

    @classmethod
    def tearDownClass(cls) -> None:
        remove(join(detect(), 'rss_reader', 'data', 'cache', 'test_cache.json'))

    def test_empty_cache(self):
        with self.assertLogs(logger='root', level='ERROR') as logs:
            self.cache.get_from_cache(date='20210531')
        self.assertIn('ERROR:root:News not found.', logs.output)

    def test_add_to_cache(self):
        with self.cache:
            for onews in news:
                self.cache.add_news_to_cache(news=onews)
        self.assertEqual(len(news), self.cache.news_count)

    def test_get_from_cache_by_date(self):
        self.assertEqual(self.cache.get_from_cache(date='20210602')[0], news[1])

    def test_get_from_cache_by_date_and_url(self):
        self.assertEqual(self.cache.get_from_cache(date='20210604', url='https://lenta.ru/rss/news')[0], news[2])
