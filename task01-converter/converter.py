"""Convert csv-file to parquet-file or vice versa. Show the schema of the file specified."""

import argparse
import re
import sys

import pyarrow.csv as csv
import pyarrow.parquet as pq

BLOCK_SIZE = 1e6


def create_parser():
    """
    Create CLI arguments parser.
    """
    usage = "converter.py [--csv2parquet | --parquet2csv <src-filename> <dst-filename>] | [--get-schema <filename>] | [--help]"
    parser = argparse.ArgumentParser(usage=usage, description=__doc__, add_help=False)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--csv2parquet", nargs=2, metavar='',
                       help="convert csv src-file to parquet dst-file")
    group.add_argument("--parquet2csv", nargs=2, metavar='',
                       help="convert parquet src-file to csv dst-file")

    parser.add_argument("--get-schema", nargs=1, metavar='',
                        help="print the file schema")
    parser.add_argument("--help", action='store_true',
                        help="show this help message and exit")

    return parser


def csv2parquet(src_file, dst_file):
    """
    Convert `src_file` csv-file to `dst_file` parquet-file.
    """
    # Setup csv-file reader
    read_options = csv.ReadOptions(block_size=BLOCK_SIZE)
    csv_reader = csv.open_csv(src_file, read_options=read_options)

    # Write parquet-file by batches
    with pq.ParquetWriter(dst_file, csv_reader.schema) as pq_writer:
        for batch in csv_reader:
            pq_writer.write_batch(batch)


def parquet2csv(src_file, dst_file):
    """
    Convert `src_file` parquet-file to `dst_file` csv-file.
    """
    # Setup parquet-file reader
    pq_reader = pq.ParquetFile(src_file)

    # Write csv-file by batches
    with csv.CSVWriter(dst_file, pq_reader.schema_arrow) as csv_writer:
        for batch in pq_reader.iter_batches():
            csv_writer.write_batch(batch)


def get_schema(src_file):
    """
    Get the schema of the `file` specified. Filetype is detected by extension.
    """
    try:
        if re.search(r"\.csv$", src_file):
            schema = csv.open_csv(src_file).schema
        elif re.search(r"\.parq(uet)?$", src_file):
            schema = pq.ParquetFile(src_file).schema_arrow
        else:
            raise Exception("Unknown file format")
    except:
        raise

    return schema.to_string()


def main():
    """
    Entry point: create args parser and process target.
    """
    arg_parser = create_parser()
    args = arg_parser.parse_args()

    try:
        if args.csv2parquet:
            src_file, dst_file = args.csv2parquet
            csv2parquet(src_file, dst_file)

        elif args.parquet2csv:
            src_file, dst_file = args.parquet2csv
            parquet2csv(src_file, dst_file)

        elif args.get_schema:
            src_file, = args.get_schema
            schema = get_schema(src_file)
            print(schema, file=sys.stdout)

        else:
            print(arg_parser.format_help(), file=sys.stdout)

    except OSError as e:
        print(f"FileError: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
