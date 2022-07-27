"""
Pure python utility to get top n movies by each genre from csv data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source filepaths specified in config file.
"""

import argparse
import configparser
import csv
import re
import sys
from collections import deque

# Global config
config = {}


def configure():
    """
    Extract script settings from config file into a global `config`.
    """
    parser = configparser.ConfigParser()
    parser.read('config.ini')

    global config

    try:
        config['movies_fpath'] = parser.get('Source', 'movies_path')
        config['ratings_fpath'] = parser.get('Source', 'ratings_path')
        config['src_encoding'] = parser.get('Source', 'encoding')
        config['src_delimiter'] = parser.get('Source', 'delimiter')

        config['dst_encoding'] = parser.get('Destination', 'encoding')
        config['dst_delimiter'] = parser.get('Destination', 'delimiter')
        config['write_schema'] = int(parser.get('Destination', 'write_schema'))

        config['title_regexp'] = parser.get('Extraction', 'title_regexp')
        config['no_genres_regexp'] = parser.get('Extraction', 'no_genres_regexp')
    except Exception:
        raise Exception("corrupted config file")


def create_parser():
    """
    Return configured parser for CLI arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)

    parser.add_argument("--N", metavar="<number>", help="top rated movies count for each genre")
    parser.add_argument("--genres", metavar="<list>", help="genres filter, list separated by '|'")
    parser.add_argument("--year_from", metavar="<year>", help="year-from  filter")
    parser.add_argument("--year_to", metavar="<year>", help="year-to  filter")
    parser.add_argument("--regexp", metavar="<regexp>", help="regexp filter for title")
    parser.add_argument("--help", action="store_true", help="show this help message and exit")

    return parser


def calc_avg_rating():
    """
    Calculate average rating from ratings csv-file.
    Return average rating storage: { movieId: avg_rating }
    """
    filepath = config['ratings_fpath']
    encoding = config['src_encoding']
    delimiter = config['src_delimiter']

    with open(filepath, encoding=encoding) as ratings_file:
        reader = csv.DictReader(ratings_file, delimiter=delimiter)

        # Raw ratings storage: { movieId: { total, count } }
        rating_storage = {}

        for row in reader:
            try:
                # Extract rating values
                movieId = int(row['movieId'])
                rating = float(row['rating'])
            except KeyError:
                raise KeyError("failed to extract data")

            # Store current row rating
            if movieId in rating_storage:
                rating_storage[movieId]['total'] += rating
                rating_storage[movieId]['count'] += 1
            else:
                rating_storage[movieId] = {}
                rating_storage[movieId]['total'] = rating
                rating_storage[movieId]['count'] = 1

        # Calc & store average ratings
        for movieId, items in rating_storage.items():
            avg_rating = items['total'] / items['count']
            rating_storage[movieId] = avg_rating

        return rating_storage


def split_title(raw_title):
    """
    Split `raw_title` string into the real title and year.
    Return them as a tuple of (title, year).
    """
    title_regexp = config['title_regexp']

    raw_title = raw_title.strip()
    re_result = re.search(title_regexp, raw_title)

    re_title, re_year = re_result.groups()
    title, year = re_title, int(re_year)

    return title, year


def split_genres(raw_genres):
    """
    Split `raw_genres` string into the genres list.
    Return genres list.
    """
    no_genres_regexp = config['no_genres_regexp']

    raw_genres = raw_genres.strip()
    re_result = re.search(no_genres_regexp, raw_genres)

    if re_result:
        raise Exception("invalid genre")

    return raw_genres.split('|')


def extract_movies():
    """
    Load all the movies and prepare dataset to filtering.
    Return movies storage: { movieId: { title, year, [genres], rating } }
    """
    rating_storage = calc_avg_rating()

    filepath = config['movies_fpath']
    encoding = config['src_encoding']
    delimiter = config['src_delimiter']

    with open(filepath, encoding=encoding) as movies_file:
        reader = csv.DictReader(movies_file, delimiter=delimiter)

        # Movies storage: [ { movieId, title, year, genre, rating } ]
        # List type chosen because of next sorting
        movies_storage = []

        for row in reader:
            # Extract values
            try:
                movieId = int(row['movieId'])
                title, year = split_title(row['title'])
                genre_list = split_genres(row['genres'])
                rating = rating_storage[movieId]
            except Exception:
                # Skip bad data
                continue

            # Store current movie
            for genre in genre_list:
                movie = {'movieId': movieId,
                         'title': title,
                         'year': year,
                         'genre': genre,
                         'rating': rating}
                movies_storage.append(movie)

    return movies_storage


def sorted_movies():
    """
    Sort movies by genre ASC, rating DESC, year DESC, title ASC
    Return sorted movies storage.
    """
    movies_storage = extract_movies()

    # Group by genre, sort by rating DESC, year DESC, title ASC.
    # Sortings should be in reversed order.
    # Built-in sort works much faster than implemented
    # with pure python cycles, but requies additional memory
    movies_storage.sort(key=lambda item: item['title'])
    movies_storage.sort(key=lambda item: item['year'], reverse=True)
    movies_storage.sort(key=lambda item: item['rating'], reverse=True)
    movies_storage.sort(key=lambda item: item['genre'])

    return movies_storage


def filter_movies(filters):
    """
    Filter movies by `filters` dictionary and store them into a deque.
    Return movies storage.
    """
    movies_storage = sorted_movies()
    result_storage = deque()

    # N is the movies count for each genre specified
    # When it's not specified all the movies should go to the output
    if filters['N'] is None:
        N = len(movies_storage)
    else:
        N = filters['N']

    # Extract all genres into a set
    genres_list = {movie['genre'] for movie in movies_storage}

    # Each genre should be count separately into this counter
    genre_counter = {genre: 0 for genre in genres_list}

    # Total movies limit is genres_size * N
    # When genres filter is not specified all the genres should go to the output
    if filters['genres'] is None:
        total_limit = len(genres_list) * N
    else:
        total_limit = len(filters['genres']) * N

    matched_movie_counter = 0

    for movie in movies_storage:
        # Filter `year from`
        if filters['year_from'] is not None:
            if movie['year'] < filters['year_from']:
                continue

        # Filter `year to`
        if filters['year_to'] is not None:
            if movie['year'] > filters['year_to']:
                continue

        # Filter `genres`
        if filters['genres'] is not None:
            if movie['genre'] not in filters['genres']:
                continue

        # Check each genre output limit
        if genre_counter[movie['genre']] >= N:
            continue

        # Filter `regexp` for title
        if filters['regexp'] is not None:
            if not re.search(filters['regexp'], movie['title']):
                continue

        # Filter `N`
        if filters['N'] is not None:
            if matched_movie_counter < total_limit:
                genre_counter[movie['genre']] += 1
                matched_movie_counter += 1
            else:
                break

        # Add movie
        matched_movie = {'genre': movie['genre'],
                         'title': movie['title'],
                         'year': movie['year'],
                         'rating': movie['rating']}
        result_storage.append(matched_movie)

    return result_storage


def main():
    """
    Entry point: configure script, get CLI args and process target.
    """
    # Set console encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

    filters = {'N': None,
               'genres': None,
               'year_from': None,
               'year_to': None,
               'regexp': None}

    try:
        configure()

        parser = create_parser()
        args = vars(parser.parse_args())

        if args['help']:
            print(parser.format_help(), file=sys.stdout)
            sys.exit(0)

        if args['N'] is not None:
            filters['N'] = int(args['N'])

        if args['genres'] is not None:
            filters['genres'] = split_genres(args['genres'])

        if args['year_from'] is not None:
            filters['year_from'] = int(args['year_from'])

        if args['year_to'] is not None:
            filters['year_to'] = int(args['year_to'])

        if args['regexp'] is not None:
            filters['regexp'] = args['regexp']

        found_movies = filter_movies(filters)

    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        sys.exit(1)

    headers = ['genre', 'title', 'year', 'rating']
    delimiter = config['dst_delimiter']
    writer = csv.DictWriter(sys.stdout, headers,
                            delimiter=delimiter,
                            lineterminator='\n')

    write_schema = config['write_schema']
    if write_schema:
        writer.writeheader()

    # Output the found data
    for row in found_movies:
        writer.writerow(row)


if __name__ == '__main__':
    main()
