import io
import datetime
import unittest
import unittest.mock

import pytz
from tzlocal import get_localzone

from rss_reader.xml_to_json import XmlJsonConverter


class TestXmlToJsonConverter(unittest.TestCase):

    def test_html_json_list(self):
        text_xml = ("<?xml version='1.0' encoding='UTF-8'?>\n"
                    "        <rss version=\"2.0\">\n"
                    "        <channel>\n"
                    "        <title>BuzzFeed News</title>\n"
                    "        <link>https://www.buzzfeednews.com</link>\n"
                    "        <language>en</language>\n"
                    "        <copyright>Copyright 2021 BuzzFeed, Inc.</copyright>\n"
                    "        <description>BuzzFeed, Reporting To You</description>\n"
                    "        <lastBuildDate>Sun, 30 May 2021 10:41:15 +0000</lastBuildDate>\n"
                    "        <image>\n"
                    "        <url>https://webappstatic.buzzfeed.com/static/images/public/rss/logo-news.png</url>\n"
                    "        <title>BuzzFeed News</title>\n"
                    "        <link>https://www.buzzfeednews.com</link>\n"
                    "        </image>\n"
                    "        <item>\n"
                    "        <title>Debt Didn’t Disappear During The Pandemic. Meet A Man Whose Job Was To Collect It."
                    "</title>\n"
                    "        <description><![CDATA[<h1>An American debt collection agency paid agents in Tijuana $150 "
                    "a week to collect from delinquent borrowers in the US. We spoke to a person who did that job "
                    "during the pandemic.</h1><p><img src=\"https://img.buzzfeed.com/buzzfeed-static/static/2021-05/"
                    "29/21/campaign_images/976d68fe3db8/debt-didnt-disappear-during-the-pandemic-meet-a-m-2-2233-"
                    "1622322661-2_dblbig.jpg\" /></p><hr /><p><a href=\"https://www.buzzfeednews.com/article/"
                    "venessawong/debt-collector-pandemic\">View Entire Post &rsaquo;</a></p>]]></description>\n"
                    "        <link>https://www.buzzfeednews.com/article/venessawong/debt-collector-pandemic</link>\n"
                    "        <pubDate>Sat, 29 May 2021 21:11:05 -0400</pubDate>\n"
                    "        <guid isPermaLink=\"false\">https://www.buzzfeednews.com/article/venessawong/debt-"
                    "collector-pandemic</guid>\n"
                    "        <category>News</category>\n"
                    "        </item>\n"
                    "        </channel>\n"
                    "        </rss>\n"
                    "        ")

        ref_dict = [{'Feed': 'BuzzFeed News',
                     'Title': 'Debt Didn’t Disappear During The Pandemic. Meet A Man Whose Job Was To Collect It.',
                     'Date': '2021-05-30 04:11:05+03:00',
                     'Link': 'https://www.buzzfeednews.com/article/venessawong/debt-collector-pandemic',
                     'Summary': '<h1>An American debt collection agency paid agents in Tijuana $150 a week to '
                                'collect from delinquent borrowers in the US. We spoke to a person who did that '
                                'job during the pandemic.</h1><p><img src="https://img.buzzfeed.com/buzzfeed-static/'
                                'static/2021-05/29/21/campaign_images/976d68fe3db8/debt-didnt-disappear-during-the-'
                                'pandemic-meet-a-m-2-2233-1622322661-2_dblbig.jpg" /></p><hr /><p><a href='
                                '"https://www.buzzfeednews.com/article/venessawong/debt-collector-pandemic">'
                                'View Entire Post &rsaquo;</a></p>',
                     'Links': {'https://www.buzzfeednews.com/article/venessawong/debt-collector-pandemic (link)': 1,
                               'https://img.buzzfeed.com/buzzfeed-static/static/2021-05/29/21/campaign_images/'
                               '976d68fe3db8/debt-didnt-disappear-during-the-pandemic-meet-a-m-2-2233-1622322661-2_'
                               'dblbig.jpg (image)': 2},
                     'URL': 'https://www.buzzfeed.com/world.xml'}]

        published_date = datetime.datetime.fromisoformat(ref_dict[0]["Date"])
        local_tzinfo = pytz.timezone(str(get_localzone()))

        published_date_local = published_date.astimezone(local_tzinfo)
        ref_dict[0]["Date"] = str(published_date_local)

        xj_conv = XmlJsonConverter(text_xml, "https://www.buzzfeed.com/world.xml")

        self.assertEqual(xj_conv._html_json_list, ref_dict)


mock_stdout = unittest.mock.patch('sys.stdout', new_callable=io.StringIO)


class TestJsonPrintMethods(unittest.TestCase):

    @mock_stdout
    def test_dump_json(self, stdout):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
        <rss>
        <channel>
        <title>BuzzFeed News</title>
        <item>
        <title>Debt Didn’t Disappear During The Pandemic.</title>
        <description> An American debt collection agency paid agents in Tijuana $150 a week </description>
        <link>https://www.buzzfeednews.com/article/venessawong/debt-collector-pandemic</link>
        <pubDate>Sat, 29 May 2021 21:11:05 EST</pubDate>
        </item>
        </channel>
        </rss>
        """
        expected = """{
  "Feed": "BuzzFeed News",
  "Title": "Debt Didn’t Disappear During The Pandemic.",
  "Date": "2021-05-30 04:11:05+03:00",
  "Link": "https://www.buzzfeednews.com/article/venessawong/debt-collector-pandemic",
  "Summary": " An American debt collection agency paid agents in Tijuana $150 a week ",
  "Links": {
    "https://www.buzzfeednews.com/article/venessawong/debt-collector-pandemic (link)": 1
  },
  "URL": "https://www.buzzfeed.com/world.xml"
}"""
        published_date = datetime.datetime.fromisoformat("2021-05-30 04:11:05+03:00")
        local_tzinfo = pytz.timezone(str(get_localzone()))

        published_date_local = str(published_date.astimezone(local_tzinfo))
        expected = expected.replace("2021-05-30 04:11:05+03:00", published_date_local)

        xjc = XmlJsonConverter(xml, "https://www.buzzfeed.com/world.xml")
        xjc.dump_json()
        actual = stdout.getvalue()

        self.assertEqual(actual, expected, "dump_json wrong output")

    @mock_stdout
    def test_dump_json_no_xml_data(self, stdout):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
        <rss>
        <channel>
        <item>
        </item>
        </channel>
        </rss>
        """
        xjc = XmlJsonConverter(xml, "")
        xjc.dump_json()

        actual = stdout.getvalue()
        expected = '{\n  "Feed": "",\n  "Title": "",\n  "Date": "",\n  "Link": "",\n  "Summary": "",\n  "Links": {},' \
                   '\n  "URL": ""\n}'
        self.assertEqual(actual, expected, "dump_json wrong output")
