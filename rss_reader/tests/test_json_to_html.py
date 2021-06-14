from rss_reader.json_to_html import HtmlJsonToHtml
import unittest
import os


class TestHtmlJsonToHtml(unittest.TestCase):

    def setUp(self) -> None:
        self.json_0 = {
            "Feed": "BuzzFeed News",
            "Title": "There Is Anger And Resignation In The Developing World As Rich Countries Buy Up All The "
                     "COVID Vaccines",
            "Date": "2020-12-30 17:25:39+03:00",
            "Link": "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world",
            "Summary": "<h1>Mexico says it's wrong for wealthy countries to buy up more vaccines than they need, "
                       "while others still don\u2019t have access to a single dose.</h1><p><img src=\"https://"
                       "img.buzzfeed.com/buzzfeed-static/static/2020-12/22/18/tmp/20f9b6998076/tmp-name-2-10554-"
                       "1608662537-20_dblbig.jpg\" /></p><hr /><p><a href=\"https://www.buzzfeednews.com/article/"
                       "karlazabludovsky/mexico-vaccine-inequality-developing-world\">View Entire Post &rsaquo;"
                       "</a></p>",
            "Links": {
                "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing"
                "-world (link)": 1,
                "https://img.buzzfeed.com/buzzfeed-static/static/2020-12/22/18/tmp/20f9b6998076/tmp-name-2-10554-"
                "1608662537-20_dblbig.jpg (image)": 2
            },
            "URL": "https://www.buzzfeed.com/world.xml"
        }
        self.json_1 = {
            "Feed": "BuzzFeed News",
            "Title": "Yes, This PE Teacher Really Danced Through The Coup In Myanmar",
            "Date": "2021-02-04 10:25:34+03:00",
            "Link": "https://www.buzzfeednews.com/article/janelytvynenko/myanmar-coup-dance",
            "Summary": "<h1>The viral video looked too absurd to be real, but online sleuths were able to quickly "
                       "verify its location.</h1><p><img src=\"https://img.buzzfeed.com/buzzfeed-static/static/"
                       "2021-02/1/21/campaign_images/f55df834b2b0/a-pe-teacher-danced-through-the-coup-in-myanmar-"
                       "2-8021-1612215221-9_dblbig.jpg\" /></p><hr /><p><a href=\"https://www.buzzfeednews.com/article"
                       "/janelytvynenko/myanmar-coup-dance\">View Entire Post &rsaquo;</a></p>",
            "Links": {
                "https://www.buzzfeednews.com/article/janelytvynenko/myanmar-coup-dance (link)": 1,
                "https://img.buzzfeed.com/buzzfeed-static/static/2021-02/1/21/campaign_images/f55df834b2b0/a-pe-"
                "teacher-danced-through-the-coup-in-myanmar-2-8021-1612215221-9_dblbig.jpg (image)": 2
            },
            "URL": "https://www.buzzfeed.com/world.xml"
        }
        self.json_list = [self.json_0, self.json_1]

        home_path = os.path.expanduser("~")
        self.file_name = os.path.join(home_path, "test-buzz-feed-news.html")

        self.url = "https://www.buzzfeed.com/world.xml"

        self.jth = HtmlJsonToHtml(self.url)

    def tearDown(self) -> None:
        try:
            os.remove(self.file_name)
        except OSError:
            pass

    def test_change_img_url(self):
        modified_html = self.jth.change_img_url(self.json_0["Summary"], "home")
        expected_html = '<html><body><h1>Mexico says it\'s wrong for wealthy countries to buy up more vaccines than ' \
                        'they need, while others still don’t have access to a single dose.</h1><p><img ' \
                        'src="home/tmp-name-2-10554-1608662537-20_dblbig.jpg"/></p><hr/><p><a ' \
                        'href="https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-' \
                        'inequality-developing-world">View Entire Post ›</a></p></body></html>'

        self.assertEqual(modified_html, expected_html, "Image URL not modified")

    def test_raw_rss2html_file(self):
        self.jth.raw_rss2html_file(self.file_name, self.json_list, True)
        self.assertEqual(os.path.isfile(self.file_name), True, f"HTML file not created: {self.file_name}")
