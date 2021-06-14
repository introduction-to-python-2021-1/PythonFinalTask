RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.   

Utility provides the following interface:

    usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source

    Pure Python command-line RSS reader.

    positional arguments:
    source         RSS URL

    optional arguments:
    -h, --help     show this help message and exit
    --version      Print version info
    --json         Print result as JSON in stdout
    --verbose      Outputs verbose status messages
    --limit LIMIT  Limit news topics if this parameter provided
    
   You are free to choose format of the news console output. The textbox below provides an example of how it can be implemented:
   
    $ rss_reader.py "https://news.yahoo.com/rss/" --limit 1
    Feed: Yahoo News - Latest News & Headlines

    Title: Nestor heads into Georgia after tornados damage Florida
    Date: Sun, 20 Oct 2019 04:21:44 +0300
    Link: https://news.yahoo.com/wet-weekend-tropical-storm-warnings-131131925.html

    [image 2: Nestor heads into Georgia after tornados damage Florida][2]Nestor raced across Georgia as a post-tropical cyclone late Saturday, hours after the former tropical storm spawned a tornado that damaged
    homes and a school in central Florida while sparing areas of the Florida Panhandle devastated one year earlier by Hurricane Michael. The storm made landfall Saturday on St. Vincent Island, a nature preserve
    off Florida's northern Gulf Coast in a lightly populated area of the state, the National Hurricane Center said. Nestor was expected to bring 1 to 3 inches of rain to drought-stricken inland areas on its
    march across a swath of the U.S. Southeast.

    Links:
    [1]: https://news.yahoo.com/wet-weekend-tropical-storm-warnings-131131925.html (link)
    [2]: http://l2.yimg.com/uu/api/res/1.2/Liyq2kH4HqlYHaS5BmZWpw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/ap.org/5ecc06358726cabef94585f99050f4f0 (image)

In case of using ```--json```  argument utility converts the news into [JSON](https://en.wikipedia.org/wiki/JSON "Описание") 

With the argument ```--verbose``` program prints all logs in stdout.

With the argument ```--date```, the app searches for news in the local storage. The local storage is replenished every time you read news from the Internet. The ```--date``` argument tells the reader to search for news not on the Internet, but in a local file. News is recorded in the local storage every time the user reads it from the Internet. The date should be specified in the yyyymmdd format.

With the ```to_pdf``` and ```to_html``` arguments, the user saves the selected news (specifies the source url) in the selected format in the selected directory (the user must specify the absolute path to the folder). The file name in the specified folder will be created automatically.  For example, user input: "https://news.yahoo.com/rss/"  --to_pdf d:/rss_news.

Examples:

--version:

    Version 1.4 - and stop running program

--json --limit 1:

    Starting reading link https://news.yahoo.com/rss/
    [
       {
          "title": "Bay Area couple accused of running multi-million dollar \u2018brothel\u2019 from apartment: report",
          "pubDate": "2021-06-14T03:12:10Z",
          "link": "https://news.yahoo.com/bay-area-couple-accused-running-031210853.html",
          "images": []
       }
    ]
    
 --date 20210604
 
    title: Psaki: No circumstance where Biden would fire Fauci
    pubDate: 2021-06-04T22:06:31Z
    link: https://news.yahoo.com/psaki-no-circumstance-where-biden-220631832.html
    images: 1
    https://s.yimg.com/hd/cp-video-transcode/prod/2021-06/04/60baa52a4cd7fe5222751540/60baa52a4cd7fe5222751541_o_U_v2.jpg

    title: A timeline of the allegations against Sienna Mae Gomez, including the video that shows her kissing Jack Wright
    pubDate: 2021-06-04T22:16:58Z
    link: https://news.yahoo.com/timeline-allegations-against-sienna-mae-221658870.html
    images: 1
    https://s.yimg.com/uu/api/res/1.2/DFuwx7ui9n9L7n5wbK9ueA--~B/aD0xNTU5O3c9MjA4NTthcHBpZD15dGFjaHlvbg-  -/https://media.zenfs.com/en/insider_articles_922/c2f7cd18b250d98acc8c054f390100eb

    title: 19-year-old tourist from California dies in stabbing on Hawaii beach, police say
    pubDate: 2021-06-04T22:00:02Z
    link: https://news.yahoo.com/19-old-tourist-california-dies-220002304.html
    images: 1
    https://s.yimg.com/uu/api/res/1.2/ca31_KE07wF.p7N4FSBlOw--~B/aD03NjA7dz0xMTQwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/kansas_city_star_mcclatchy_articles_677/43cc83a75c5f8a6057e8444f9babc506



 
 
