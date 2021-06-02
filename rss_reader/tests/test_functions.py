import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock
from unittest.mock import patch
from urllib.error import URLError
import os

from reader.article import Article
from reader import functions


class TestFunctions(unittest.TestCase):
    """Test cases to test functions"""

    def setUp(self):
        self.url = 'Some_URL'
        self.url_b = 'https://news.yahoo.com/rss/'
        self.article_a = Article('Japan reporter freed from Myanmar says inmates were abused',
                                 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html',
                                 '2021-05-21T15:03:25Z', 'Associated Press', '---',
                                 'https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAwMDthcHB'
                                 'pZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc')
        self.article_b = Article('Title_B', 'Link_B', '2021-05-22T15:03:25Z', 'Source_B', 'Description_B', 'Image_B')
        self.entries = [{'title': 'Japan reporter freed from Myanmar says inmates were abused',
                         'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://news.yahoo.com/rss/',
                                          'value': 'Japan reporter freed from Myanmar says inmates were abused'},
                         'links': [{'rel': 'alternate', 'type': 'text/html',
                                    'href': 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html'}],
                         'link': 'https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html',
                         'published': '2021-05-21T15:03:25Z',
                         'published_parsed': 'time.struct_time(tm_year=2021, tm_mon=5, tm_mday=21, tm_hour=8, tm_min=21'
                                             ', tm_sec=38, tm_wday=4, tm_yday=141, tm_isdst=0)',
                         'source': {'href': 'http://www.ap.org/', 'title': 'Associated Press'},
                         'id': 'japan-reporter-freed-myanmar-says-082138070.html', 'guidislink': False,
                         'media_content': [{'height': '86',
                                            'url': 'https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOT'
                                                   'k4O3c9MzAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.'
                                                   'org/d2d71e1fafaffbdd78bb05538e0732dc',
                                            'width': '130'}], 'media_credit': [{'role': 'publishing company'}],
                         'credit': ''}]
        self.json = '{\n    "Title": "Japan reporter freed from Myanmar says inmates were abused",\n' \
                    '    "Link": "https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html",\n' \
                    '    "Date": "Fri, 21 May, 2021",\n' \
                    '    "Source": "Associated Press",\n' \
                    '    "Description": "---",\n' \
                    '    "Image": "https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAw' \
                    'MDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc"\n}'
        self.html = '<html title="RSS news">\n\
  <head>\n\
    <meta charset="utf-8">\n\
  </head>\n\
  <h1>Japan reporter freed from Myanmar says inmates were abused</h1>\n\
  <p>\n\
    <b>Title: </b>Japan reporter freed from Myanmar says inmates were abused\n\
  </p>\n\
  <p>\n\
    <b>Link: \n\
      <a href="https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html">\n\
        <b>https://news.yahoo.com/japan-reporter-freed-myanmar-says-082138070.html</b>\n\
      </a>\n\
    </b>\n\
  </p>\n\
  <p>\n\
    <b>Date: </b>Fri, 21 May, 2021\n\
  </p>\n\
  <p>\n\
    <b>Source: </b>Associated Press\n\
  </p>\n\
  <p>\n\
    <b>Description: </b>---\n\
  </p>\n\
  <p>\n\
    <img src="https://s.yimg.com/uu/api/res/1.2/oj6L3nekcGoPEQVuv9hvqA--~B/aD0xOTk4O3c9MzAwMDthcHBpZD15dGFjaHlvbg--\
/https://media.zenfs.com/en/ap.org/d2d71e1fafaffbdd78bb05538e0732dc" style="width:360px">\n\
  </p>\n\
</html>'

    def test_parse_news(self):
        """Checks that processing the entries creates an object of the Article class"""
        self.actual = functions.parse_news(self.entries)[0]
        self.assertEqual(self.actual, self.article_a)

    def test_empty_news(self):
        """Checks that the program exits after recieving an empty input"""
        self.entries = {'entries': []}

        with self.assertRaises(SystemExit) as cm:
            functions.parse_news(self.entries)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Sorry, no news to parse!")

    def test_make_json(self):
        """Checks that news is converted to json format correctly"""
        self.assertEqual(functions.make_json(self.article_a), self.json)

    def test_check_limit(self):
        """Tests check_limit function with valid values (positive numbers)"""
        self.assertEqual(functions.check_limit('2'), 2)

    def test_check_limit_value_error(self):
        """Tests check_limit function with unvalid values (letters)"""
        with self.assertRaises(SystemExit) as cm:
            functions.check_limit('symbol')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be a positive number')

    def test_check_limit_negative(self):
        """Tests check_limit function with unvalid values (negative numbers)"""
        with self.assertRaises(SystemExit) as cm:
            functions.check_limit('-10')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be greater than 0')

    def test_check_limit_zero(self):
        """Tests check_limit function with unvalid values (zero)"""
        with self.assertRaises(SystemExit) as cm:
            functions.check_limit('0')

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'The argument "limit" should be greater than 0')

    @patch('feedparser.parse')
    def test_bad_link(self, mock_api_call):
        """Tests get_from_url function if url returns empty news list"""
        mock_api_call.return_value = {'entries': []}
        with self.assertRaises(SystemExit) as cm:
            functions.get_from_url(self.url)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Please, check if the entered link is correct!")

    @patch('feedparser.parse')
    def test_unvalid_url(self, mock_api_call):
        """Tests get_from_url function if url is not available"""
        mock_api_call.side_effect = MagicMock(side_effect=URLError('foo'))
        with self.assertRaises(SystemExit) as cm:
            functions.get_from_url(self.url)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Source isn't available")

    @patch('feedparser.parse')
    def test_valid_url(self, parser):
        """Tests get_from_url function if url returns correct news list"""
        parser.return_value = {'entries': self.entries}

        self.actual = functions.get_from_url(self.entries)
        self.assertEqual(self.actual[0], self.article_a)

    def test_version_only(self):
        """Checks that the program stops after printing a version when --version is specified"""
        with io.StringIO() as term_value, redirect_stdout(term_value):
            with self.assertRaises(SystemExit):
                functions.create_arguments([None, '--version'])
                self.assertEqual(term_value.getvalue(), 'Version 1.3')

    def test_version_and_other_arg(self):
        """Checks that the program stops after printing a version when --version and another arg are specified"""
        with io.StringIO() as term_value, redirect_stdout(term_value):
            with self.assertRaises(SystemExit):
                functions.create_arguments([None, self.url, '--version'])
                self.assertEqual(term_value.getvalue(), 'Version 1.3')

    def test_json_args(self):
        """Checks that create_arguments function correctly recognizes passed arguments"""
        self.actual = functions.create_arguments([None, self.url, '--json'])
        self.assertTrue(self.actual['json'])

    def test_execute_news(self):
        """Checks if --source and --date are specified the execute_news function will execute the required sql query"""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_logger = MagicMock()
        date = '20210521'
        functions.execute_news(date, mock_connection, self.url, mock_logger)
        self.assertEqual(mock_cursor.execute.call_args.args[0], 'SELECT title, link, full_date, source, description, '
                                                                'image, url FROM news WHERE date=:date and url=:url')
        self.assertEqual(mock_cursor.execute.call_args.args[1]['date'], date)
        self.assertEqual(mock_cursor.execute.call_args.args[1]['url'], self.url)

    def test_execute_news_without_url(self):
        """Checks if only --date is specified the execute_news function will execute the required sql query"""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_logger = MagicMock()
        date = '20210521'
        functions.execute_news(date, mock_connection, None, mock_logger)
        self.assertEqual(mock_cursor.execute.call_args.args[0],
                         'SELECT title, link, full_date, source, description, image, url FROM news WHERE date=:date')
        self.assertEqual(mock_cursor.execute.call_args.args[1]['date'], date)

    def test_valid_path_to_directory(self):
        """Checks that the specified path exists"""
        path = os.path.abspath(os.curdir)
        mock_logger = MagicMock(return_value=None)
        self.actual = functions.check_path_to_directory(path, mock_logger)
        self.assertEqual(self.actual, True)

    def test_non_existent_folder(self):
        """Tests check_path_to_directory function if the folder does not exist"""
        path = 'C:/Test/Test/Test/Test'
        mock_logger = MagicMock(return_value=None)
        with self.assertRaises(NotADirectoryError) as cm:
            functions.check_path_to_directory(path, mock_logger)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], 'Entered path is invalid: folder does not exist')

    @patch('reader.functions.check_path_to_directory')
    def test_save_news_in_html(self, checker):
        """Checks that the function is converting the passed object to html-format"""
        checker.return_value = True
        path = os.path.abspath(os.curdir)
        mock_logger = MagicMock(return_value=None)
        html = functions.save_news_in_html_file([self.article_a], path, mock_logger)
        with io.StringIO() as term_value, redirect_stdout(term_value):
            f = open(html.name, 'r')
            print(f.read())
            self.assertEqual(term_value.getvalue(), self.html + '\n')
            f.close()
        os.remove(html.name)

    @patch('reader.functions.save_news_in_html_file')
    def test_save_news_in_pdf(self, html_saver):
        """Checks that the function is converting the passed object to pdf-format"""
        path = os.path.abspath(os.curdir)
        mock_logger = MagicMock(return_value=None)
        html_file = os.path.join(path, 'test.html')
        with open(html_file, 'x', encoding='utf-8') as html:
            html.write(self.html)
        html_saver.return_value = html
        pdf = functions.save_news_in_pdf_file(self.article_a, path, mock_logger)
        html.close()
        self.assertTrue(os.path.join(path, 'rss_news.pdf'))
        os.remove(pdf.name)


if __name__ == "__main__":
    unittest.main()
