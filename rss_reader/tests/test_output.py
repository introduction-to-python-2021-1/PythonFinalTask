from io import StringIO
from unittest import TestCase
from unittest.mock import Mock, patch

from modules.output import ConsoleOutput
from tests.data.news_list import news

output = """
Feed: RT World News

Title: China criticizes US for being ‘world’s number one secret stealer’ after reports of NSA spying
Date: Fri, 04 Jun 2021 11:02:52 +0000
Link: https://www.rt.com/news/525559-china-us-france-germany-spies/

 The Chinese Foreign Ministry has issued a stern rebuke of US intelligence 

Links:
[1] https://www.rt.com/news/525559-china-us-france-germany-spies/ (link)
[2] https://cdni.rt.com/files/2021.06/thumbnail/60b8b5b620302731b846dd9b.JPG (image)
"""

output_json = """[
   {
      "url": "https://www.rt.com/rss/news/",
      "feed": "RT World News",
      "title": "China criticizes US for being ‘world’s number one secret stealer’ after reports of NSA spying",
      "link": "https://www.rt.com/news/525559-china-us-france-germany-spies/",
      "date": "Fri, 04 Jun 2021 11:02:52 +0000",
      "description": " The Chinese Foreign Ministry has issued a stern rebuke of US intelligence ",
      "links": [
         {
            "link": "https://www.rt.com/news/525559-china-us-france-germany-spies/",
            "type": "link"
         },
         {
            "link": "https://cdni.rt.com/files/2021.06/thumbnail/60b8b5b620302731b846dd9b.JPG",
            "type": "image"
         }
      ]
   }
]
"""


class TestConsoleOutput(TestCase):

    def setUp(self) -> None:
        self.output = ConsoleOutput(logger=Mock())

    @patch('sys.stdout', new_callable=StringIO)
    def test_output(self, mock_stdout):
        self.output.output(news, limit=1)
        self.assertEqual(mock_stdout.getvalue(), output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_output_json(self, mock_stdout):
        self.output.output_json(news, limit=1)
        self.assertEqual(mock_stdout.getvalue(), output_json)
