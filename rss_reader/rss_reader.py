"""
rss_reader.py - receives URL from the command line and read the data from it and output it in STDOUT
"""
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='RSS reader - a command-line utility which receives URL '
                    'and prints results in human-readable format'
    )

    parser.add_argument('rss_url', help="RSS url to parse")
    parser.add_argument('--version', action="version", help="Print version info", version='Version 1.0')
    parser.add_argument('--json', help="Print result as JSON in stdout", action="store_true")
    parser.add_argument('--verbose', action="store_true", help="Outputs verbose status messages")
    parser.add_argument('--limit', type=int, help="Limit news topics if this parameter provided", default=0)

    args = parser.parse_args()
    print(args)

    try:
        if args.verbose:
            print("Verbosity is turned on")

        limit = args.limit
        if args.verbose:
            print(f"Limit is {limit}")

        json = args.json
        if args.verbose:
            print(f"json is {json}")

    except argparse.ArgumentError:
        print("Catching an argumentError")


try:
    get_args()
except Exception as e:
    print(f"Exception message: {e}")


#
# def main():
#     try:
#         get_args()
#     except Exception as e:
#         print(f"Exception message: {e}")
#
#
# if __name__ == "__main__":
#     main()