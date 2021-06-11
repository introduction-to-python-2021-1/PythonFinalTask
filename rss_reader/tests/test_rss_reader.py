import unittest
from io import StringIO
from unittest.mock import patch
from unittest import TestCase

from src.rss_reader import main, __version__


class TestRssReader(TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_version(self, MockStdout):
        argv = ['None', '--version']
        main(argv)
        version = f'Version is {__version__}\n'
        self.assertEqual(MockStdout.getvalue(), version)


if __name__ == '__main__':
    unittest.main()
