# Get-movies

Pure python utility to get top n movies by each genre from csv-data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source filepaths specified in config file.

## Requirements

The utility requires [**`python3`**](https://www.python.org/downloads/) interpreter with [**`pip`**](https://pypi.org/project/pip/) installing tool.

On the command line the interpreter can be typed as `python`, `python3`, `py` (depending on OS, version, etc.).

To be specific this readme has decided to use the interpreter name `python` in the examples.

## Usage

All options are optional. To show help message below use `--help` option.

```sh
usage: get-movies.py [--N <number>] [--genres <list>] [--year_from <year>] [--year_to <year>] [--regexp <regexp>] [--help]

Pure python utility to get top n movies by each genre from csv data. Outputs to the stdout in csv-like format: (genre, title,     
year, rating). Source filepaths specified in config file.

options:
  --N <number>        top rated movies count for each genre
  --genres <list>     genres filter, list separated by '|'
  --year_from <year>  year-from filter
  --year_to <year>    year-to filter
  --regexp <regexp>   regexp filter for title
  --help              show this help message and exit
```

All filters can be combined in any combination.
Output is always grouped by genre and sorted by rating DESC, year DESC, title ASC. 

## Examples

- Get all movies for each genre
```sh
> python get-movies.py
  
genre,title,year,rating
Action,Tokyo Tribe,2014,5.0
Action,Justice League: Doom,2012,5.0
Action,On the Other Side of the Tracks (De l'autre côté du périph),2012,5.0
Action,Faster,2010,5.0
Action,Superman/Batman: Public Enemies,2009,5.0
...
```

- Get 3 top rated movies for both "Sci-Fi" and "War" genres:
```sh
> python get-movies.py --N 3 --genres "Sci-Fi|War"
  
genre,title,year,rating
Sci-Fi,SORI: Voice from the Heart,2016,5.0
Sci-Fi,The Girl with All the Gifts,2016,5.0
Sci-Fi,Delirium,2014,5.0
War,Battle For Sevastopol,2015,5.0
War,Che: Part One,2008,5.0
War,Che: Part Two,2008,5.0
```

- Get 3 top rated movies with title containing "the" or "The" for "Sci-Fi" genre released from 1999 to 2000 year:
```sh
> python get-movies.py --N 3 --regexp ".[Tt]he " --genre "Sci-Fi" --year_from 1999 --year_to 2000

genre,title,year,rating
Sci-Fi,Batman Beyond: Return of the Joker,2000,3.5
Sci-Fi,Star Wars: Episode I - The Phantom Menace,1999,3.107142857142857
Sci-Fi,Universal Soldier: The Return,1999,2.625
```

## Configuration

Configuration file `config.ini` should be stored next to the script. It should contain:

**[Source]**

- `movies_path` — input movies.csv filepath
- `ratings_path` — input ratings.csv filepath
- `encoding` — input files encoding
- `delimiter` — input files delimiter

**[Destination]**

- `encoding` — output data encoding
- `delimiter` — output data delimiter
- `write_schema` — enable output schema 

**[Extraction]**

- `title_regexp` — regular expression to split raw title into the real title and year
- `no_genres_regexp` — regular expression to detect movies with no genre

## Source data

Source files should be downloaded from [grouplens.org](https://grouplens.org/datasets/movielens/):

- [MovieLens Latest Dataset (small)](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)
- [MovieLens Latest Dataset](https://files.grouplens.org/datasets/movielens/ml-latest.zip)
- [MovieLens 25M Dataset](https://files.grouplens.org/datasets/movielens/ml-25m.zip)

Example files included in the `data/` directory.

### Download utility

Additional shell utility allowes to download and extract source files automatically.

Usage of the utility:

```sh
setup.sh --ds small|medium|stable
```
