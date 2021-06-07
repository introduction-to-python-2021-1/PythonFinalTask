import io
import unittest
import unittest.mock

from rss_reader.json_to_json import HtmlJsonToTextJson


class TestJsonToJsonConverter(unittest.TestCase):

    def setUp(self) -> None:
        self.json_0 = {
  "Feed": "BuzzFeed News",
  "Title": "There Is Anger And Resignation In The Developing World As Rich Countries Buy Up All The COVID Vaccines",
  "Date": "2020-12-30 17:25:39+03:00",
  "Link": "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world",
  "Summary": "<h1>Mexico says it's wrong for wealthy countries to buy up more vaccines than they need, while others "
             "still don\u2019t have access to a single dose.</h1><p><img src=\"https://img.buzzfeed.com/buzzfeed-"
             "static/static/2020-12/22/18/tmp/20f9b6998076/tmp-name-2-10554-1608662537-20_dblbig.jpg\" /></p><hr />"
             "<p><a href=\"https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing"
             "-world\">View Entire Post &rsaquo;</a></p>",
  "Links": {
    "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world (link)": 1,
    "https://img.buzzfeed.com/buzzfeed-static/static/2020-12/22/18/tmp/20f9b6998076/tmp-name-2-10554-"
    "1608662537-20_dblbig.jpg (image)": 2
  }
}

        self.json_1 = {
  "Feed": "BuzzFeed News",
  "Title": "Yes, This PE Teacher Really Danced Through The Coup In Myanmar",
  "Date": "2021-02-04 10:25:34+03:00",
  "Link": "https://www.buzzfeednews.com/article/janelytvynenko/myanmar-coup-dance",
  "Summary": "<h1>The viral video looked too absurd to be real, but online sleuths were able to quickly verify its"
             " location.</h1><p><img src=\"https://img.buzzfeed.com/buzzfeed-static/static/2021-02/1/21/campaign"
             "_images/f55df834b2b0/a-pe-teacher-danced-through-the-coup-in-myanmar-2-8021-1612215221-9_dblbig.jpg\""
             " /></p><hr /><p><a href=\"https://www.buzzfeednews.com/article/janelytvynenko/myanmar-coup-dance\">"
             "View Entire Post &rsaquo;</a></p>",
  "Links": {
    "https://www.buzzfeednews.com/article/janelytvynenko/myanmar-coup-dance (link)": 1,
    "https://img.buzzfeed.com/buzzfeed-static/static/2021-02/1/21/campaign_images/f55df834b2b0/a-pe-teacher-"
    "danced-through-the-coup-in-myanmar-2-8021-1612215221-9_dblbig.jpg (image)": 2
  }
}

        self.json_2 = {
  "Feed": "BuzzFeed News",
  "Title": "Twitter Is Blocking Tweets That Criticize How The Indian Government Has Handled The Pandemic",
  "Date": "2021-04-26 09:25:38+03:00",
  "Link": "https://www.buzzfeednews.com/article/pranavdixit/twitter-blocking-tweets-india",
  "Summary": "<h1>More than 50 tweets are now blocked in India.</h1><p><img src=\"https://img.buzzfeed.com/"
             "buzzfeed-static/static/2021-04/25/23/campaign_images/03f6839c6b5d/twitter-is-blocking-tweets-that-"
             "criticize-how-the-2-2255-1619394031-12_dblbig.jpg\" /></p><hr /><p><a href=\"https://www.buzzfeednews."
             "com/article/pranavdixit/twitter-blocking-tweets-india\">View Entire Post &rsaquo;</a></p>",
  "Links": {
    "https://www.buzzfeednews.com/article/pranavdixit/twitter-blocking-tweets-india (link)": 1,
    "https://img.buzzfeed.com/buzzfeed-static/static/2021-04/25/23/campaign_images/03f6839c6b5d/twitter-is-blocking-"
    "tweets-that-criticize-how-the-2-2255-1619394031-12_dblbig.jpg (image)": 2
  }
}

        self.json_list = [self.json_0, self.json_1, self.json_2]

        self.text_json_0 = {
  "Feed": "BuzzFeed News",
  "Title": "There Is Anger And Resignation In The Developing World As Rich Countries Buy Up All The COVID Vaccines",
  "Date": "Wed, 30 Dec 2020 17:25:39 +0300",
  "Link": "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world",
  "Summary": "Mexico says it's wrong for wealthy countries to buy up more vaccines than they need, while others still"
             " don’t have access to a single dose. [image [2] ] [link [1] View Entire Post ›]",
  "Links": {
    "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world (link)": 1,
    "https://img.buzzfeed.com/buzzfeed-static/static/2020-12/22/18/tmp/20f9b6998076/tmp-name-2-10554-1608662537-20"
    "_dblbig.jpg (image)": 2
  }
}
        self.text_json_1 = {
  "Feed": "BuzzFeed News",
  "Title": "Yes, This PE Teacher Really Danced Through The Coup In Myanmar",
  "Date": "Thu, 04 Feb 2021 10:25:34 +0300",
  "Link": "https://www.buzzfeednews.com/article/janelytvynenko/myanmar-coup-dance",
  "Summary": "The viral video looked too absurd to be real, but online sleuths were able to quickly verify its "
             "location. [image [2] ] [link [1] View Entire Post ›]",
  "Links": {
    "https://www.buzzfeednews.com/article/janelytvynenko/myanmar-coup-dance (link)": 1,
    "https://img.buzzfeed.com/buzzfeed-static/static/2021-02/1/21/campaign_images/f55df834b2b0/a-pe-teacher-danced-t"
    "hrough-the-coup-in-myanmar-2-8021-1612215221-9_dblbig.jpg (image)": 2
  }
}
        self.text_json_2 = {
  "Feed": "BuzzFeed News",
  "Title": "Twitter Is Blocking Tweets That Criticize How The Indian Government Has Handled The Pandemic",
  "Date": "Mon, 26 Apr 2021 09:25:38 +0300",
  "Link": "https://www.buzzfeednews.com/article/pranavdixit/twitter-blocking-tweets-india",
  "Summary": "More than 50 tweets are now blocked in India. [image [2] ] [link [1] View Entire Post ›]",
  "Links": {
    "https://www.buzzfeednews.com/article/pranavdixit/twitter-blocking-tweets-india (link)": 1,
    "https://img.buzzfeed.com/buzzfeed-static/static/2021-04/25/23/campaign_images/03f6839c6b5d/twitter-is-blocking"
    "-tweets-that-criticize-how-the-2-2255-1619394031-12_dblbig.jpg (image)": 2
  }
}
        self.expected_text_json_list = [self.text_json_0, self.text_json_1, self.text_json_2]

    def test_xml2html_json_limited(self):
        entries_limit = 2
        j2j = HtmlJsonToTextJson(self.json_list, limit=entries_limit)
        self.assertEqual(j2j.text_json_list, self.expected_text_json_list[:entries_limit], "JSON conversion error")

    def test_xml2html_json(self):

        j2j = HtmlJsonToTextJson(self.json_list)
        self.assertEqual(j2j.text_json_list, self.expected_text_json_list, "JSON conversion error")

    mock_stdout = unittest.mock.patch('sys.stdout', new_callable=io.StringIO)

    @mock_stdout
    def test_dump_json(self, stdout):
        j2j = HtmlJsonToTextJson(self.json_list)
        j2j.dump_json(1)
        actual_output = stdout.getvalue()
        expected_output = """{
  "Feed": "BuzzFeed News",
  "Title": "There Is Anger And Resignation In The Developing World As Rich Countries Buy Up All The COVID Vaccines",
  "Date": "Wed, 30 Dec 2020 17:25:39 +0300",
  "Link": "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world",
  "Summary": "Mexico says it's wrong for wealthy countries to buy up more vaccines than they need, while others still don’t have access to a single dose. [image [2] ] [link [1] View Entire Post ›]",
  "Links": {
    "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world (link)": 1,
    "https://img.buzzfeed.com/buzzfeed-static/static/2020-12/22/18/tmp/20f9b6998076/tmp-name-2-10554-1608662537-20_dblbig.jpg (image)": 2
  }
}
"""
        self.assertEqual(actual_output, expected_output, "JSON dump error")

    @mock_stdout
    def test_print_json(self, stdout):
        j2j = HtmlJsonToTextJson(self.json_list)
        j2j.print_json(1)
        actual_output = stdout.getvalue()
        expected_output = """--------------------------------------------------------------------------------
Feed: BuzzFeed News
Title: There Is Anger And Resignation In The Developing World As Rich Countries Buy Up All The COVID Vaccines
Date: Wed, 30 Dec 2020 17:25:39 +0300
Link: https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world

Summary: Mexico says it's wrong for wealthy countries to buy up more vaccines than they need, while others still don’t have access to a single dose. [image [2] ] [link [1] View Entire Post ›]

Links:
[1] https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world (link)
[2] https://img.buzzfeed.com/buzzfeed-static/static/2020-12/22/18/tmp/20f9b6998076/tmp-name-2-10554-1608662537-20_dblbig.jpg (image)
"""
        self.assertEqual(actual_output, expected_output, "JSON print error")

    @mock_stdout
    def test_print_json_empty_list(self, stdout):
        j2j = HtmlJsonToTextJson([])
        j2j.print_json()
        actual_output = stdout.getvalue()
        expected_output = "RSS feed data not available\n"
        self.assertEqual(actual_output, expected_output, "empty JSON list print error")

    @mock_stdout
    def test_dump_json_empty_list(self, stdout):
        j2j = HtmlJsonToTextJson([])
        j2j.dump_json()
        actual_output = stdout.getvalue()
        expected_output = "RSS feed data not available\n"
        self.assertEqual(actual_output, expected_output, "empty JSON list print error")
