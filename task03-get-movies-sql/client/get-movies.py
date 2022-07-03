"""
Python/MySQL utility to get top n movies by each genre from csv data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source filepaths specified in config file.
"""

import argparse
import configparser
import csv
import sys

import mysql.connector

config = {}


def configure():
    """
    Extract script settings from config file into a variable.
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
    except Exception:
        sys.stderr.write("Exception: corrupted config file")
        sys.exit(1)


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
    except Exception as e:
        sys.stderr.write(f"Exception: {e}\n")

    try:
        connection = mysql.connector.connect(
            database=config['database'],
            host=config['host'],
            user=config['user'],
            password=config['password']
        )

        cursor = connection.cursor(dictionary=True)
        cursor.callproc(config['proc_get_top_n_movies'], list(filters.values()))

        headers = ['genre', 'title', 'year', 'rating']
        writer = csv.DictWriter(sys.stdout, headers)

        writer.writeheader()

        # Output the found data
        for cur in cursor.stored_results():
            found_movies = cur.fetchall()
            for movie in found_movies:
                writer.writerow(movie)

    except mysql.connector.Error as e:
        sys.stderr.write(f"MySQLError: {e}\n")
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    main()
