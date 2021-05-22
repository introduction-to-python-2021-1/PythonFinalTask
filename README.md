## Usage

```shell 
usage: rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] 
                  [source]

Pure Python command-line RSS reader.

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limit news topics if this parameter provided
```

## JSON structure

<pre>
[
   {
      "feed": "FOX Sports Digital",
      "title": "Charlie Blackmon clubs third home run, Rockies beat Diamondbacks, 7-6",
      "link": "https://www.foxsports.com/mlb/video/1900336707885",
      "date": "Sat, 22 May 2021 22:38:09 +0000",
      "description": "Charlie Blackmon hit his third home run of the season in the Colorado Rockies’ 7-6 win over the Arizona Diamondbacks.",
      "links": [
         {
            "link": "https://www.foxsports.com/mlb/video/1900336707885",
            "type": "link"
         },
         {
            "link": "https://b.fssta.com/uploads/2021/05/blackmon-1.vresize.335.220.high.0.png",
            "type": "image"
         }
      ]
   }
]
</pre>
