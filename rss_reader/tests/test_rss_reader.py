import logging
import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from rss_reader.src.rss_reader import main, __version__, create_logger


class TestRssReader(TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_version(self, MockStdout):
        argv = ['None', '--version']
        main(argv)
        version = f'Version is {__version__}\n'
        self.assertEqual(MockStdout.getvalue(), version)

    def test_create_logger(self):
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger()
        self.assertEqual(logger, create_logger())


if __name__ == '__main__':
    unittest.main()
