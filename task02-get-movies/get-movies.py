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

        config['title_regexp'] = parser.get('Settings', 'title_regexp')
        config['no_genres_regexp'] = parser.get('Settings', 'no_genres_regexp')
    except Exception:
        sys.stderr.write("Exception: corrupted config file")
        sys.exit(-1)


def create_parser():
    """
    Create configured parser for CLI arguments.
    """
    usage = "get-movies.py [--N <number>] | [--genres <list>] | [--year_from <year>] | [--year_to <year>] | [--regexp <regular-expression>] | [--help]"
    description = "Select top n of the most rated movies."
    parser = argparse.ArgumentParser(usage=usage, description=description, add_help=False)

    parser.add_argument("--N", metavar='', help="quantity of the most rated movies")
    parser.add_argument("--genres", metavar='', help="genres filter")
    parser.add_argument("--year_from", metavar='', help="start year")
    parser.add_argument("--year_to", metavar='', help="end year")
    parser.add_argument("--regexp", metavar='', help="regexp filter")
    parser.add_argument("--help", action='store_true', help="show this help message and exit")

    return parser


def calc_avg_rating():
    """
    Calculate average rating from ratings csv-file.
    Return average rating storage: { movieId: avg_rating }
    """
    with open(config['ratings_fpath'], encoding=config['src_encoding']) as ratings_file:
        reader = csv.DictReader(ratings_file, delimiter=config['src_delimiter'])

        # Raw ratings storage: { movieId: { total, count } }
        rating_storage = {}

        for row in reader:
            try:
                # Extract rating values
                movieId = int(row['movieId'])
                rating = float(row['rating'])
            except KeyError:
                sys.stderr.write("KeyError: failed to extract data")
                sys.exit(-1)

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
    Split raw title string into the real title and year.
    """
    raw_title = raw_title.strip()
    re_result = re.search(config['title_regexp'], raw_title)
    try:
        title = re_result.groups()[0]
        year = int(re_result.groups()[1])
    except:
        raise Exception

    return title, year


def split_genres(raw_genres):
    """
    Split raw genres string into the genres list.
    """
    raw_genres = raw_genres.strip()
    re_result = re.search(config['no_genres_regexp'], raw_genres)
    if not re_result:
        return raw_genres.split('|')
    else:
        raise Exception


def extract_movies():
    """
    Load all the movies and prepare dataset to filtering.
    Return movies storage: { movieId: { title, year, [genres], rating } }
    """
    rating_storage = calc_avg_rating()

    with open(config['movies_fpath'], encoding=config['src_encoding']) as movies_file:
        reader = csv.DictReader(movies_file, delimiter=config['src_delimiter'])

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
            except:
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


def filter_movies(filters):
    """
    Store movies filtered with `filters`.
    """
    try:
        movies_storage = extract_movies()
    except Exception as e:
        sys.stderr.write(f"Exception: {e}")
        sys.exit(-1)

    # Group by genre, sort by rating DESC, year DESC, title ASC (in reversed order)
    # Built-in sort works much faster than implemented with pure python cycles, but requies additional memory
    movies_storage.sort(key=lambda item: item['title'])
    movies_storage.sort(key=lambda item: item['year'], reverse=True)
    movies_storage.sort(key=lambda item: item['rating'], reverse=True)
    movies_storage.sort(key=lambda item: item['genre'])

    result_storage = deque()

    # When limit not specified all the movies should go to the output
    if filters['N'] is None:
        movies_limit = len(movies_storage)
    else:
        movies_limit = filters['N']

    # Extract all genres into a set
    genres_list = {movie['genre'] for movie in movies_storage}

    # Each genre should be count separately into this counter
    genre_counter = {genre: 0 for genre in genres_list}

    # Total movies limit is movies_limit * genres_size
    # When genres filter not specified all the genres should go to the output
    if filters['genres'] is None:
        total_limit = len(genres_list) * movies_limit
    else:
        total_limit = len(filters['genres']) * movies_limit

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
        if genre_counter[movie['genre']] >= movies_limit:
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
    configure()

    parser = create_parser()
    args = vars(parser.parse_args(sys.argv[1:]))

    filters = {'N': None,
               'genres': None,
               'year_from': None,
               'year_to': None,
               'regexp': None}

    try:
        if args['help']:
            sys.stdout.write(parser.format_help())
            return
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
    except OSError as e:
        sys.stderr.write(f"FileError: {e}\n")
    except BaseException as e:
        sys.stderr.write(f"Exception: {e}\n")

    found_movies = filter_movies(filters)

    headers = ['genre', 'title', 'year', 'rating']
    writer = csv.DictWriter(sys.stdout, headers, delimiter=config['dst_delimiter'])

    if config['write_schema']:
        writer.writeheader()

    # Output the found data
    for row in found_movies:
        writer.writerow(row)


if __name__ == '__main__':
    main()
