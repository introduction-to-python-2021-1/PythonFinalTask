import parser_debug as psr
from feed_Container import feed_Container


def main():
    parser = psr.args_Parser()

    feed = feed_Container(url = parser.args_Space.source)

    feed.print_feed_Info()
    feed.print_items(limit = parser.args_Space.limit)

if __name__ == '__main__':
    main()



