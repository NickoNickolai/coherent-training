"""
Python/Hadoop-streaming utility to get top n movies by each genre from csv data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source files should be uploaded into HDFS.
"""

import argparse
import configparser
import json
import os
import sys

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
        config['src_delimiter'] = parser.get('Source', 'delimiter')

        config['dst_delimiter'] = parser.get('Destination', 'delimiter')

        config['title_regexp'] = parser.get('Extraction', 'title_regexp')
        config['no_genres_regexp'] = parser.get('Extraction', 'no_genres_regexp')

        config['executor'] = parser.get('Engine', 'executor')
    except Exception:
        raise Exception("corrupted config file")


def create_parser():
    """
    Return configured parser for CLI arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)

    parser.add_argument("--N", metavar="<number>", help="movies count for each genre")
    parser.add_argument("--genres", metavar="<list>", help="genres filter, list separated by '|'")
    parser.add_argument("--year_from", metavar="<year>", help="year-from  filter")
    parser.add_argument("--year_to", metavar="<year>", help="year-to  filter")
    parser.add_argument("--regexp", metavar="<regexp>", help="regexp filter for title")
    parser.add_argument("--help", action="store_true", help="show this help message and exit")

    return parser


def main():
    """
    Entry point: configure script, get CLI args and process target.
    """
    # Set console encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

    try:
        configure()

        mapreduce_args = {
            'src_delimiter': config['src_delimiter'],
            'dst_delimiter': config['dst_delimiter'],
            'title_regexp': config['title_regexp'],
            'no_genres_regexp': config['no_genres_regexp'],
            'N': None,
            'genres': None,
            'year_from': None,
            'year_to': None,
            'regexp': None
        }

        parser = create_parser()
        args = vars(parser.parse_args())

        if args['help']:
            print(parser.format_help(), file=sys.stdout)
            sys.exit(0)

        if args['N'] is not None:
            mapreduce_args['N'] = int(args['N'])

        if args['genres'] is not None:
            mapreduce_args['genres'] = args['genres']
  
        if args['year_from'] is not None:
            mapreduce_args['year_from'] = int(args['year_from'])

        if args['year_to'] is not None:
            mapreduce_args['year_to'] = int(args['year_to'])

        if args['regexp'] is not None:
            mapreduce_args['regexp'] = args['regexp']

        cmd_template = "sudo docker exec -it cloudera_quickstart {} '{}'"
        cmd = cmd_template.format(config['executor'], json.dumps(mapreduce_args))
        os.system(cmd)

    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
