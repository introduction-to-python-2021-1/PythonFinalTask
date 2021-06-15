Structure of JSON used in rss_reader:

    XML conveted to JSON by the following cheme:

    Format conversion:
    -----------------
    XML key -> JSON key
    'title' -> 'Feed'
    'item'/'title' -> 'Title'
    'item'/'pubDate' -> 'Date'
    'item'/'link' -> 'Link'
    'item'/'description' -> 'Summary'

    XML 'pubDate' converted to local timezone and saved to JSON in ISO format:
    XML 'pubDate' = 'Sun, 31 May 2021 09:00:17 -0400'
    JSON 'Date' = '2021-05-31 16:00:17+03:00'

    EST time 'Sun, 31 May 2021 09:00:17 EST' considered to be equal to '-0400'
    timezone 'Sun, 31 May 2021 09:00:17 -0400'

    JSON value for key 'Links' contains links collected from JSON 'Link' and 'Summary' keys values

    URL value is arsg.source parameter in main() method

    json_entry = {
        "Feed": "",
        "Title": "",
        "Date": "", 
        "Link": "", 
        "Summary": "", 
        "Links": {}
        "URL": ""
                    }

    Example of HTML JSON used for storage:

    html_json_entry = {
        "Feed": "Reuters News Agency",
        "Title": "Reuters reveals Porsche, Piech families weigh direct stake in possible Porsche IPO; market reacts",
        "Date": "2021-06-01 18:25:46+03:00",
        "Link": "https://www.reutersagency.com/en/reuters-best/reuters-reveals-porsche-piech-families-weigh-direct-stake-in-possible-porsche-ipo-market-reacts/",
        "Summary": "<p>Shares in Europe\u2019s largest carmaker Volkswagen climbed for a second consecutive day after Reuters revealed that the powerful Porsche and [&#8230;]</p>\n<p>The post <a rel=\"nofollow\" href=\"https://www.reutersagency.com/en/reuters-best/reuters-reveals-porsche-piech-families-weigh-direct-stake-in-possible-porsche-ipo-market-reacts/\">Reuters reveals Porsche, Piech families weigh direct stake in possible Porsche IPO; market reacts</a> appeared first on <a rel=\"nofollow\" href=\"https://www.reutersagency.com/en/\">Reuters News Agency</a>.</p>\n",
        "Links": {
            "https://www.reutersagency.com/en/reuters-best/reuters-reveals-porsche-piech-families-weigh-direct-stake-in-possible-porsche-ipo-market-reacts/ (link)": 1,
            "https://www.reutersagency.com/en/ (link)": 2
                }
        "URL": "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best"
        }

    Example of text JSON used for printing:

    text_json_entry = {
        "Feed": "Reuters News Agency",
        "Title": "Reuters reveals Porsche, Piech families weigh direct stake in possible Porsche IPO; market reacts",
        "Date": "Tue, 01 Jun 2021 18:25:46 +0300",
        "Link": "https://www.reutersagency.com/en/reuters-best/reuters-reveals-porsche-piech-families-weigh-direct-stake-in-possible-porsche-ipo-market-reacts/",
        "Summary": "Shares in Europe’s largest carmaker Volkswagen climbed for a second consecutive day after Reuters revealed that the powerful Porsche and […]\nThe post  [link [1] Reuters reveals Porsche, Piech families weigh direct stake in possible Porsche IPO; market reacts] appeared first on  [link [2] Reuters News Agency].\n",
        "Links": 
            {
            "https://www.reutersagency.com/en/reuters-best/reuters-reveals-porsche-piech-families-weigh-direct-stake-in-possible-porsche-ipo-market-reacts/ (link)": 1,
            "https://www.reutersagency.com/en/ (link)": 2
            }
        }

    JSON storage organized the followind way:
        user home directory~/.rss_reader/url directory/date directory/JSON files

        for html_json_entry path will be:
        home/username/.rss_reader/httpswwwreutersagencycomfeedtaxonomybestsectorsposttypebest/20210601/182546.json

