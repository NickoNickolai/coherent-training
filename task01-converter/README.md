# Converter

Convert csv-file to parquet-file or vice versa. Show the schema of the file specified.

## Requirements

The utility requires [**`python3`**](https://www.python.org/downloads/) interpreter with [**`pip`**](https://pypi.org/project/pip/) installing tool.

On the command line the interpreter can be typed as `python`, `python3`, `py` (depending on OS, version, etc.).

To be specific this readme has decided to use the interpreter name `python` in the examples.

## Dependencies

All extra packages listed in the `requirements.txt`:

- [**`pyarrow`**](https://arrow.apache.org/docs/python/index.html) `8.0.0` — Python API for Arrow and the leaf libraries that add additional functionality such as reading Apache Parquet files into Arrow structures.

To install extra packages automatically set the working directory to the project root and execute:

```sh
> python -m pip install -r requirements.txt
```

## Usage

To show help message below use `--help` argument.

```sh
usage: converter.py [--csv2parquet | --parquet2csv <src-filename> <dst-filename>] | [--get-schema <filename>] | [--help]

Convert csv-file to parquet-file or vice versa. Show the schema of the file specified.

options:
  --csv2parquet    convert csv src-file to parquet dst-file
  --parquet2csv    convert parquet src-file to csv dst-file
  --get-schema     print the file schema
  --help           show this help message and exit
```

## Examples

- Convert csv-file to parquet-file:
  ```sh
  > python converter.py --csv2parquet <src-filename> <dst-filename>
  ```

- Convert parquet-file to csv-file:
  ```sh
  > python converter.py --parquet2csv <src-filename> <dst-filename>
  ```

- Get file schema:
  ```sh
  > python converter.py --get-schema <filename>
  ```
