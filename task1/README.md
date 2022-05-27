
# Converter

A simple csv/parquet console app converter.
Can convert csv-file to parquet-file or vice versa and show the schema of the file specified.


## Options

- **--csv2parquet** *<src-filename> <dst-filename>* — convert csv src-file to parquet dst-file
- **--parquet2csv** *<src-filename> <dst-filename>* — convert parquet src-file to csv dst-file
- **--get-schema** *<filename>* — print the file schema
- **--help** — show this help message and exit

## Usage

Convert csv to parquet:
```
convert.py --csv2parquet <src-filename> <dst-filename>
```

Convert parquet to csv:
```
convert.py --parquet2csv <src-filename> <dst-filename>
```

Get file schema:
```
convert.py --get-schema <filename>
```

Show help message:
```
convert.py --help
```

## Dependencies

- pandas
```
python -m pip install pandas
```
- pyarrow
```
python -m pip install pyarrow
```
