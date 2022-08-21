"""
Python/MySQL utility to get top n movies by each genre from csv data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source filepaths specified in config file.
"""

import argparse
import configparser
import csv
import sys
from collections import deque

import mysql.connector

config = {}


def configure():
    """
    Extract script settings from config file into a global `config`.
    """
    parser = configparser.ConfigParser()
    parser.read('config.ini')

    global config

    try:
        config['database'] = parser.get('db', 'database')
        config['host'] = parser.get('db', 'host')
        config['user'] = parser.get('db', 'user')
        config['password'] = parser.get('db', 'password')
        config['proc_get_top_n_movies'] = parser.get('db', 'proc_get_top_n_movies')

        config['dst_encoding'] = parser.get('Destination', 'encoding')
        config['dst_delimiter'] = parser.get('Destination', 'delimiter')
        config['write_schema'] = int(parser.get('Destination', 'write_schema'))
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


def filter_movies(filters):
    """
    Filter movies by `filters` dictionary.
    Return filtered movies list.
    """
    connection = None
    cursor = None
    found_movies = deque()

    try:
        connection = mysql.connector.connect(
            database=config['database'],
            host=config['host'],
            user=config['user'],
            password=config['password']
        )

        cursor = connection.cursor(dictionary=True)
        cursor.callproc(config['proc_get_top_n_movies'], list(filters.values()))

        for cur in cursor.stored_results():
            found_movies.extend(cur.fetchall())

        return found_movies

    except Exception:
        raise

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def print_movies(found_movies):
    """
    Print found movies in the csv-like format to stdout.
    """
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
            filters['genres'] = args['genres']

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

    print_movies(found_movies)


if __name__ == '__main__':
    main()
