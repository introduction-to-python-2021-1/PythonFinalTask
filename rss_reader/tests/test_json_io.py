import random
import unittest
import os
import shutil
import requests_mock

from rss_reader.json_io import JsonIO


class TestJsonIO(unittest.TestCase):

    def setUp(self) -> None:
        self.json_0 = {
            "Feed": "BuzzFeed News",
            "Title": "There Is Anger And Resignation In The Developing World As Rich Countries Buy Up All "
                     "The COVID Vaccines",
            "Date": "2020-12-30 17:25:39+03:00",
            "Link": "https://www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing-world",
            "Summary": "<h1>Mexico says it's wrong for wealthy countries to buy up more vaccines than they need, "
                       "while others still don\u2019t have access to a single dose.</h1><p><img src=\"https://"
                       "img.buzzfeed.com/buzzfeed-static/static/2020-12/22/18/tmp/20f9b6998076/"
                       "tmp-name-2-10554-1608662537-20_dblbig.jpg\" /></p><hr /><p><a href=\"https://"
                       "www.buzzfeednews.com/article/karlazabludovsky/mexico-vaccine-inequality-developing"
                       "-world\">View Entire Post &rsaquo;</a></p>",
            "Links": {
                "https://www.buzzfeednews.com/article/karlazabludovsky/"
                "mexico-vaccine-inequality-developing-world (link)": 1,
                "https://img.buzzfeed.com/20f9b6998076/tmp-name-2-10554-1608662537-20_dblbig.jpg (image)": 2
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
                       "2021-02/1/21/campaign_images/f55df834b2b0/a-pe-teacher-danced-through-the-coup-in-myanmar"
                       "-2-8021-1612215221-9_dblbig.jpg\" /></p><hr /><p><a href=\"https://www.buzzfeednews.com/"
                       "article/janelytvynenko/myanmar-coup-dance\">View Entire Post &rsaquo;</a></p>",
            "Links": {
                "https://www.buzzfeednews.com/article/janelytvynenko/myanmar-coup-dance (link)": 1,
                "https://img.buzzfeed.com/a-pe-teacher-danced-through-the-coup-in-myanmar_dblbig.jpg (image)"
                "": 2
            },
            "URL": "https://www.buzzfeed.com/world.xml"
        }

        self.json_2 = {
            "Feed": "BuzzFeed News",
            "Title": "Twitter Is Blocking Tweets That Criticize How The Indian Government Has Handled The Pandemic",
            "Date": "2021-04-26 09:25:38+03:00",
            "Link": "https://www.buzzfeednews.com/article/pranavdixit/twitter-blocking-tweets-india",
            "Summary": "<h1>More than 50 tweets are now blocked in India.</h1><p><img src=\"https://img.buzzfeed.com/"
                       "buzzfeed-static/static/2021-04/25/23/campaign_images/03f6839c6b5d/twitter-is-blocking-tweets"
                       "-that-criticize-how-the-2-2255-1619394031-12_dblbig.jpg\" /></p><hr /><p><a href=\"https://"
                       "www.buzzfeednews.com/article/pranavdixit/twitter-blocking-tweets-india\">"
                       "View Entire Post &rsaquo;</a></p>",
            "Links": {
                "https://www.buzzfeednews.com/article/pranavdixit/twitter-blocking-tweets-india (link)": 1,
                "https://img.buzzfeed.com/twitter-is-blocking-tweets-that-criticize-how-the_dblbig.jpg (image)": 2
            },
            "URL": "https://www.buzzfeed.com/world.xml"
        }

        self.url = "https://www.buzzfeed.com/world.xml"

        self.dir_name = ".rss_pars" + str(random.randint(1000, 9999))

        self.json_list = [self.json_0, self.json_1, self.json_2]

        self.jio = JsonIO(dirname=self.dir_name)

    def tearDown(self) -> None:
        home_path = os.path.expanduser("~")
        dir_path = os.path.join(home_path, self.dir_name)
        try:
            shutil.rmtree(dir_path)
        except OSError:
            pass

    def test_get_base_directory_path(self):
        home_path = os.path.expanduser("~")
        expected_path = os.path.join(home_path, self.dir_name)
        self.assertEqual(self.jio.get_base_directory_path(), expected_path)

    def test_save_and_load_raw_rss(self):
        # saving prepared list of dictionaries
        self.jio.save_raw_rss(self.json_list)
        # loading dictionaries from the storage
        # checking saved entry 0
        loaded_list = self.jio.load_raw_rss("20201230", "https://www.buzzfeed.com/world.xml")
        self.assertEqual(loaded_list[0], self.json_list[0], "saved and loaded data not match")
        # checking saved entry 1
        loaded_list = self.jio.load_raw_rss("20210204", "https://www.buzzfeed.com/world.xml")
        self.assertEqual(loaded_list[0], self.json_list[1], "saved and loaded data not match")
        # checking saved entry 2
        loaded_list = self.jio.load_raw_rss("20210426", "https://www.buzzfeed.com/world.xml")
        self.assertEqual(loaded_list[0], self.json_list[2], "saved and loaded data not match")

    def test_save_and_find_raw_rss(self):
        # saving prepared list of dictionaries
        self.jio.save_raw_rss(self.json_list)
        # loading dictionaries from the storage
        # checking saved entry 0
        loaded_list = self.jio.find_raw_rss("20201230", "")

        self.assertEqual(loaded_list[0], self.json_list[0], "saved and loaded data not match")
        # checking saved entry 1
        loaded_list = self.jio.find_raw_rss("20210204", "")

        self.assertEqual(loaded_list[0], self.json_list[1], "saved and loaded data not match")
        # checking saved entry 2
        loaded_list = self.jio.find_raw_rss("20210426", "")

        self.assertEqual(loaded_list[0], self.json_list[2], "saved and loaded data not match")

    @requests_mock.mock()
    def test_download_images(self, m):
        self.jio.save_raw_rss(self.json_list)
        picture_data_stub = "picture"
        url_1 = "https://img.buzzfeed.com/20f9b6998076/tmp-name-2-10554-1608662537-20_dblbig.jpg"
        url_2 = "https://img.buzzfeed.com/a-pe-teacher-danced-through-the-coup-in-myanmar_dblbig.jpg"
        url_3 = "https://img.buzzfeed.com/twitter-is-blocking-tweets-that-criticize-how-the_dblbig.jpg"
        m.get(url_1, text=picture_data_stub)
        m.get(url_2, text=picture_data_stub)
        m.get(url_3, text=picture_data_stub)
        self.jio.download_images(self.json_list, "https://www.buzzfeed.com/world.xml")

        base_path = self.jio.get_base_directory_path()

        path_1 = os.path.join(base_path, "httpswwwbuzzfeedcomworldxml", "20201230",
                              "tmp-name-2-10554-1608662537-20_dblbig.jpg")
        self.assertEqual(os.path.isfile(path_1), True, "Picture file not created")

        path_2 = os.path.join(base_path, "httpswwwbuzzfeedcomworldxml", "20210204",
                              "a-pe-teacher-danced-through-the-coup-in-myanmar_dblbig.jpg")
        self.assertEqual(os.path.isfile(path_2), True, "Picture file not created")

        path_3 = os.path.join(base_path, "httpswwwbuzzfeedcomworldxml", "20210426",
                              "twitter-is-blocking-tweets-that-criticize-how-the_dblbig.jpg")
        self.assertEqual(os.path.isfile(path_3), True, "Picture file not created")
