Pure Python command-line RSS reader.

This rss_reader receives RSS URL and prints results in human-readable format.


Interface example: 

    usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] 
                        source
    
    Pure Python command-line RSS reader
    
    positional arguments:
      source         RSS URL
    
    optional arguments:
      -h, --help     show this help message and exit
      --version      Print version info
      --json         Print result as JSON in stdout
      --verbose      Outputs verbose status messages
      --limit LIMIT  Limit news topics if this parameter provided


JSON structure:

    {
        article = {
                'Title': title,
                'Link': link,
                'Date': pubDate,
                'Source': source,
                'Description': description,
                'Image': imageLink,
        }
    }