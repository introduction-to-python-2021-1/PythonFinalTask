news = [
    {
        "url": "https://www.rt.com/rss/news/",
        "feed": "RT World News",
        "title": "title1",
        "link": "https://www.url1.com/",
        "date": "Fri, 04 Jun 2021 11:02:52 +0000",
        "description": "description1",
        "links": [
            {
                "link": "https://www.url1.com",
                "type": "link"
            },
            {
                "link": "https://www.url1.com/image",
                "type": "image"
            }
        ]
    },
    {
        "url": "https://www.rt.com/rss/news/",
        "feed": "RT World News",
        "title": "title2",
        "link": "https://www.url2.com/",
        "date": "Wed, 02 Jun 2021 14:32:59 +0000",
        "links": [
            {
                "link": "https://www.url2.com",
                "type": "link"
            },
            {
                "link": "https://www.url2.com/image",
                "type": "image"
            }
        ]
    },
    {
        "url": "https://lenta.ru/rss/news",
        "feed": "Lenta.ru : Новости",
        "title": "title3",
        "link": "https://www.url3.com/",
        "date": "Fri, 04 Jun 2021 13:13:00 +0300",
        "description": "description2"
    }
]

output = """
Feed: RT World News

Title: title1
Date: Fri, 04 Jun 2021 11:02:52 +0000
Link: https://www.url1.com/

description1

Links:
[1] https://www.url1.com (link)
[2] https://www.url1.com/image (image)

Feed: RT World News

Title: title2
Date: Wed, 02 Jun 2021 14:32:59 +0000
Link: https://www.url2.com/

Links:
[1] https://www.url2.com (link)
[2] https://www.url2.com/image (image)

Feed: Lenta.ru : Новости

Title: title3
Date: Fri, 04 Jun 2021 13:13:00 +0300
Link: https://www.url3.com/

description2

"""

output_json = """[
   {
      "url": "https://www.rt.com/rss/news/",
      "feed": "RT World News",
      "title": "title1",
      "link": "https://www.url1.com/",
      "date": "Fri, 04 Jun 2021 11:02:52 +0000",
      "description": "description1",
      "links": [
         {
            "link": "https://www.url1.com",
            "type": "link"
         },
         {
            "link": "https://www.url1.com/image",
            "type": "image"
         }
      ]
   },
   {
      "url": "https://www.rt.com/rss/news/",
      "feed": "RT World News",
      "title": "title2",
      "link": "https://www.url2.com/",
      "date": "Wed, 02 Jun 2021 14:32:59 +0000",
      "links": [
         {
            "link": "https://www.url2.com",
            "type": "link"
         },
         {
            "link": "https://www.url2.com/image",
            "type": "image"
         }
      ]
   },
   {
      "url": "https://lenta.ru/rss/news",
      "feed": "Lenta.ru : Новости",
      "title": "title3",
      "link": "https://www.url3.com/",
      "date": "Fri, 04 Jun 2021 13:13:00 +0300",
      "description": "description2"
   }
]
"""

output_first = """
Feed: RT World News

Title: title1
Date: Fri, 04 Jun 2021 11:02:52 +0000
Link: https://www.url1.com/

description1

Links:
[1] https://www.url1.com (link)
[2] https://www.url1.com/image (image)
"""
