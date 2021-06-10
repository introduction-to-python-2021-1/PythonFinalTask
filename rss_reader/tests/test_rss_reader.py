import unittest
from io import StringIO
from unittest.mock import patch, Mock

from modules.argparser import Argparser
from rss_reader.rss_reader.rss_reader import main, __version__


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.argparser = Argparser(logger=Mock())

    @patch('sys.stdout', new_callable=StringIO)
    def test_version(self, mock_stdout):
        argv = ['None', '--version']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), '\nVersion {}\n'.format(__version__))

    @patch('sys.stdout', new_callable=StringIO)
    def test_version_with_source(self, mock_stdout):
        argv = ['None', 'https://news.yahoo.com/rss/', '--version']
        main(argv)
        self.assertEqual(mock_stdout.getvalue(), '\nVersion {}\n'.format(__version__))


if __name__ == '__main__':
    unittest.main()
