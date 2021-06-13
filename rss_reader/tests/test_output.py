from unittest import TestCase
from unittest.mock import patch

from rss_reader.src.rss_reader import create_logger

input_parameters = {
    'new 0': {
        'feed': 'Yahoo News - Latest News & Headlines',
        'title': 'Undervaccinated red states are nowhere near herd immunity as dangerous Delta variant'
                 ' spreads',
        'date': '2021-06-11T09:00:52Z',
        'link': 'https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as'
                '-dangerous-delta-variant-spreads-090052183.html',
        'links': {
            'link 0': {
                'href': 'https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-'
                        'immunity-as-dangerous-delta-variant-spreads-090052183.html',
                'type': 'text/html'
            }
        }
    }
}

default_output = ["""
Feed: Yahoo News - Latest News & Headlines
Title: Undervaccinated red states are nowhere near herd immunity as dangerous Delta variant spreads
Date: 2021-06-11T09:00:52Z
Link: https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as-dangerous-delta-variant
-spreads-090052183.html
Links:
[1]: https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as-dangerous-delta-variant
-spreads-090052183.html (text/html)
"""]

json_output = {
    "new 0": {
        "feed": "Yahoo News - Latest News & Headlines",
        "title": "Undervaccinated red states are nowhere near herd immunity as dangerous Delta variant spreads",
        "date": "2021-06-11T09:00:52Z",
        "link": "https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as-dangerous-delta-variant-spreads-090052183.html",
        "links": {
            "link 0": {
                "href": "https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as-dangerous-delta-variant-spreads-090052183.html",
                "type": "text/html"
            }
        }
    }
}


class TestOutput(TestCase):
    def setUp(self) -> None:
        self.logger = create_logger()

    @patch('src.modules.output.DefaultOutput')
    def test_default_output(self, MockDefaultOutput):
        console_output = MockDefaultOutput()
        console_output.output.return_value = console_output
        response = console_output.output(input_parameters)
        self.assertEqual(response, console_output.output.return_value)

    @patch('src.modules.output.JSONOutput')
    def test_json_output(self, MockJSONOutput):
        console_output = MockJSONOutput()
        console_output.output.return_value = console_output
        response = console_output.output(json_output)
        self.assertEqual(response, console_output.output.return_value)
