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
