import unittest
from io import StringIO
from os import remove
from os.path import join
from unittest.mock import patch, Mock

from rootpath import detect

from modules.argparser import Argparser
from rss_reader.rss_reader.rss_reader import main, __version__

news_dir = join(detect(), 'rss_reader', 'data', 'example', 'news.xml')
with open(news_dir, 'r') as file:
    news = file.read()
first_news = """
Feed: Lenta.ru : Новости

Title: Путин раскрыл число привившихся россиян
Date: Sat, 12 Jun 2020 16:48:07 +0300
Link: https://lenta.ru/news/2021/06/12/malovato/

Президент России Владимир Путин заявил, что с начала вакцинации в России привились 18 миллионов человек

Links:
[1] https://lenta.ru/news/2021/06/12/malovato/ (link)
[2] https://icdn.lenta.ru/images/ (image)
"""

second_news = """
Feed: Lenta.ru : Новости

Title: В центре Гамалеи рассказали о влиянии индийского штамма на привитых от COVID-19
Date: Sat, 12 Jun 2020 16:42:17 +0300
Link: https://lenta.ru/news/2021/06/12/niz/

Индийский штамм коронавируса снижает в несколько раз иммунный ответ у привившихся от коронавируса

Links:
[1] https://lenta.ru/news/2021/06/12/niz/ (link)
[2] https://icdn.lenta.ru/images/2021/06/12/16 (image)
"""
third_news = """
Feed: Lenta.ru : Новости

Title: Раскрыта готовность двух первых «самых крутых» самолетов в мире
Date: Sat, 12 Jun 2020 16:34:00 +0300
Link: https://lenta.ru/news/2021/06/12/b21/

Американская военно-промышленная корпорация Northrop Grumman практически завершила производство

Links:
[1] https://lenta.ru/news/2021/06/12/b21/ (link)
[2] https://icdn.lenta.ru/images/2021/06/11/12/ (image)
"""


class TestMain(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        remove(join(detect(), 'rss_reader', 'data', 'cache', 'cache.json'))

    def setUp(self) -> None:
        self.argparser = Argparser(logger=Mock())

    @patch('sys.stdout', new_callable=StringIO)
    def test_version(self, mock_stdout):
        """ Test program with the given version argument """
        argv = ['None', '--version']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), '\nVersion {}\n'.format(__version__))

    @patch('sys.stdout', new_callable=StringIO)
    def test_version_with_source(self, mock_stdout):
        """ Test program with the given version and source arguments """
        argv = ['None', 'https://news.yahoo.com/rss/', '--version']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), '\nVersion {}\n'.format(__version__))

    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_source(self, mock_stdout, mock_get):

        mock_get.return_value.text = news
        argv = ['None', 'https://www.test.com/rss/news']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), first_news + second_news + third_news)

    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_source_with_limit(self, mock_stdout, mock_get):
        """ Test program with the given source argument """
        mock_get.return_value.text = news
        argv = ['None', 'https://www.test.com/rss/news', '--limit=1']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), first_news)

    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_source_with_date(self, mock_stdout, mock_get):
        """ Test program with the given source and date arguments """
        mock_get.return_value.text = news
        argv = ['None', 'https://www.test.com/rss/news', '--date=20200612']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), third_news + second_news + first_news)


if __name__ == '__main__':
    unittest.main()
