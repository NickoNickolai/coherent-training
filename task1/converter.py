#!/usr/bin/python3

import argparse
import re
import sys
import pandas as pd


def createParser():
    """
    CLI arguments parser.
    """
    usage = "converter.py [--csv2parquet | --parquet2csv <src-filename> <dst-filename>] | [--get-schema <filename>] | [--help]"
    description = "Convert csv-file to parquet-file or vice versa. Show the schema of the file specified."
    parser = argparse.ArgumentParser(usage=usage, description=description, add_help=False)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--csv2parquet", nargs=2, metavar='', help="convert csv src-file to parquet dst-file")
    group.add_argument("--parquet2csv", nargs=2, metavar='', help="convert parquet src-file to csv dst-file")

    parser.add_argument("--get-schema", nargs=1, metavar='', help="print the file schema")
    parser.add_argument("--help", action='store_true', help="show this help message and exit")

    return parser


def csv2parquet(src, dst, encoding='utf-8'):
    """
    Convert `src` csv-file to `dst` parquet-file. For csv-file `encoding` param is available.
    """
    df = pd.read_csv(src, encoding=encoding)
    df.to_parquet(dst, index=False)


def parquet2csv(src, dst, encoding='utf-8'):
    """
    Convert `src` parquet-file to `dst` csv-file. For csv-file `encoding` param is available.
    """
    df = pd.read_parquet(src)
    df.to_csv(dst, index=False, encoding=encoding)


def get_schema(file):
    """
    Print to console the schema of the `file` specified.
    """
    try:
        df = pd.read_csv(file)
    except (FileNotFoundError, PermissionError):
        raise
    except BaseException as e:
        try:
            df = pd.read_parquet(file)
        except (FileNotFoundError, PermissionError):
            raise
        except BaseException as e:
            raise Exception("Unknown file format")
    print(re.split("\ndtype:", str(df.dtypes))[0])


def main():
    """
    Entry point: create args parser and process target.
    """
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.csv2parquet:
            csv2parquet(args.csv2parquet[0], args.csv2parquet[1])
        elif args.parquet2csv:
            parquet2csv(args.parquet2csv[0], args.parquet2csv[1])
        elif args.get_schema:
            get_schema(args.get_schema[0])
        else:
            parser.print_help()
    except (FileNotFoundError, PermissionError) as e:
        print(f"FileError: {e}")
    except BaseException as e:
        print(f"Exception: {e}")


if __name__ == '__main__':
    main()
