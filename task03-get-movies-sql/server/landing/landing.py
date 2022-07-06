"""
Python/MySQL utility to get top n movies by each genre from csv data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source filepaths specified in config file.
"""

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

        config['movies_fpath'] = parser.get('Source', 'movies_path')
        config['ratings_fpath'] = parser.get('Source', 'ratings_path')
        config['src_encoding'] = parser.get('Source', 'encoding')
        config['src_delimiter'] = parser.get('Source', 'delimiter')

        config['movies_tbl'] = parser.get('Destination', 'movies_tbl')
        config['ratings_tbl'] = parser.get('Destination', 'ratings_tbl')

        config['chunk_size'] = int(parser.get('Settings', 'chunk_size'))
    except Exception as e:
        sys.stderr.write(f"Exception: corrupted config file: {e}")
        sys.exit(1)


def land_movies():
    """
    Store data from movies.csv into the landing table.
    """
    connection = mysql.connector.connect(
        database=config['database'],
        host=config['host'],
        user=config['user'],
        password=config['password']
    )

    cursor = connection.cursor()

    with open(config['movies_fpath'], encoding=config['src_encoding']) as f:
        reader = csv.DictReader(f, delimiter=config['src_delimiter'])

        print("Load movies")

        chunk_counter = 0
        chunk_string_list = []
        chunk_values_list = []

        query_head = f"insert into {config['movies_tbl']} (movieId, title, genres) values "

        for i, row in enumerate(reader):
            movieId = row['movieId']
            title = row['title']
            genres = row['genres']

            chunk_string_list.append("(%s, %s, %s)")
            chunk_values_list.extend([movieId, title, genres])

            if chunk_counter < config['chunk_size'] - 1:
                chunk_counter += 1
            else:   
                query = query_head + ','.join(chunk_string_list)

                cursor.execute(query, chunk_values_list)
                connection.commit()

                chunk_counter = 0
                chunk_string_list = []
                chunk_values_list = []

                print(f"{i+1} records inserted")

        query = query_head + ','.join(chunk_string_list)

        cursor.execute(query, chunk_values_list)
        connection.commit()

        print(f"{i+1} records inserted")

    cursor.close()
    connection.close()


def land_ratings():
    """
    Store data from ratings.csv into the landing table.
    """
    connection = mysql.connector.connect(
        database=config['database'],
        host=config['host'],
        user=config['user'],
        password=config['password']
    )

    cursor = connection.cursor()

    with open(config['ratings_fpath'], encoding=config['src_encoding']) as f:
        reader = csv.DictReader(f, delimiter=config['src_delimiter'])

        print("Load ratings")

        chunk_counter = 0
        chunk_values_list = []

        query_head = f"insert into {config['ratings_tbl']} (movieId, rating) values "

        for i, row in enumerate(reader):

            movieId = row['movieId']
            rating = row['rating']

            chunk_values_list.append(f"({movieId}, {rating})")

            if chunk_counter < config['chunk_size'] - 1:
                chunk_counter += 1
            else:   
                query = query_head + ','.join(chunk_values_list)
                chunk_counter = 0
                chunk_values_list = []

                cursor.execute(query)
                connection.commit()

                print(f"{i+1} records inserted")
        
        query = query_head + ','.join(chunk_values_list)
        cursor.execute(query)
        connection.commit()
        print(f"{i+1} records inserted")

    cursor.close()
    connection.close()


def main():
    """
    Entry point: load data into the landing.
    """
    configure()

    # Load movies.csv
    land_movies()

    # Load ratings.csv
    land_ratings()


if __name__ == '__main__':
    main()
