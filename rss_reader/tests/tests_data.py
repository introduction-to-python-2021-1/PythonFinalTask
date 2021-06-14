XML_INFO = """<?xml version="1.0" encoding="UTF-8"?>
            <rss xmlns:media="http://search/">
               <channel>
                  <title>Chanel title</title>
                  <link>Chanel link</link>
                  <description>Chanel description</description>
                  <item>
                     <title>News title</title>
                     <link>News link</link>
                     <pubDate>News date</pubDate>
                     <guid>news id</guid>
                     <media:content url="Media url" />
                  </item>
                  <item>
                     <title>News title</title>
                     <link>News link</link>
                     <pubDate>News date</pubDate>
                     <guid>news id</guid>
                     <media:content url="Media url" />
                  </item>
               </channel>
            </rss>"""

RSS_JSON = """[
    {
        "Link": "Chanel link",
        "Description": "Chanel description",
        "Title": "Chanel title",
        "News": [
            {
                "Title": "News title",
                "Date": "News date",
                "Link": "News link",
                "Media": [
                    "Media url"
                ]
            }
        ]
    }
]
"""
