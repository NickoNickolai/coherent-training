import csv
import json
import re
import sys

# Global CLI arguments storage
args = {}


def get_args():
    """
    Get CLI arguments into a dict storage.
    """
    global args
    args = json.loads(sys.argv[1])


def split_title(raw_title):
    """
    Split `raw_title` string into the real title and year.
    Return them as a tuple of (title, year).
    """
    raw_title = raw_title.strip()
    re_result = re.search(args['title_regexp'], raw_title)

    re_title, re_year = re_result.groups()
    title, year = re_title, int(re_year)

    return title, year


def split_genres(raw_genres):
    """
    Split `raw_genres` string into the genres list.
    Return genres list.
    """
    raw_genres = raw_genres.strip()
    re_result = re.search(args['no_genres_regexp'], raw_genres)

    if re_result:
        raise Exception("invalid genre")

    return raw_genres.split('|')


def map(line):
    """
    Mapper function for mapreduce flow.
    Yield `genre, (year, title)` pair.
    """
    csv_reader = csv.reader([line], delimiter=args['src_delimiter'].encode('utf-8'))
    csv_values = next(csv_reader)
    _, raw_title, raw_genres = csv_values

    genres_list = split_genres(raw_genres)

    for genre in genres_list:
        try:
            title, year = split_title(raw_title)

            # Filter `year from`
            if args['year_from'] is not None:
                if year < int(args['year_from']):
                    continue

            # Filter `year to`
            if args['year_to'] is not None:
                if year > int(args['year_to']):
                    continue

            # Filter `genres`
            if args['genres'] is not None:
                if genre not in split_genres(args['genres']):
                    continue

            # Filter `regexp` for title
            if args['regexp'] is not None:
                if not re.search(args['regexp'], title):
                    continue

            yield genre, (title, year)

        except Exception:
            # Skip bad data
            continue


def main():
    """
    Entry point: get CLI args and process mapping.
    """
    get_args()

    for line in sys.stdin:
        try:
            for key, value in map(line):
                genre = key
                title, year = value
                print("%s\t%s\t%s" % (genre, title, year))
        except Exception:
            continue


if __name__ == '__main__':
    main()
