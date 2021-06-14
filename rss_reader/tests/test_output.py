from io import StringIO
from unittest import TestCase
from unittest.mock import Mock, patch

from modules.output import ConsoleOutput
from rss_reader.rss_reader.rss_reader import create_logger
from tests.data.news_list import news, output, output_json, output_first


class TestConsoleOutput(TestCase):
    """ Class for testing console output module """

    def setUp(self) -> None:
        self.output = ConsoleOutput(logger=Mock())

    @patch('sys.stdout', new_callable=StringIO)
    def test_output(self, mock_stdout):
        """ Checking the news output to the console """
        self.output.output(news, limit=False)
        self.assertEqual(mock_stdout.getvalue(), output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_output_with_negative_limit(self, mock_stdout):
        """ Checking the output of news to the console with a negative limit """
        self.output.output(news, limit=-999)
        self.assertEqual(mock_stdout.getvalue(), output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_output_with_limit(self, mock_stdout):
        """ Checking news output to the console with a limit """
        self.output.output(news, limit=1)
        self.assertEqual(mock_stdout.getvalue(), output_first)

    @patch('sys.stdout', new_callable=StringIO)
    def test_output_json(self, mock_stdout):
        """ Checking news output in JSON format """
        self.output.output_json(news, limit=False)
        self.assertEqual(mock_stdout.getvalue(), output_json)

    def test_output_manager(self):
        """ Checking context manager for console output """
        with self.assertLogs(logger='root', level='DEBUG') as logs:
            with ConsoleOutput(logger=create_logger()):
                pass
        self.assertIn('DEBUG:root:News printing has started.', logs.output)
        self.assertIn('DEBUG:root:News printing has finished.', logs.output)
