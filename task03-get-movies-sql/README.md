# Get-movies

Python/MySQL utility to get top n movies by each genre from csv-data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source files should be loaded into MySQL database.

## Structure

Get-movies utility consists of server-side and client-side parts.

- `server/` directory contains landing script and sql-scripts

- `client/` directory contains get-movies utility

## Usage

The utility can handle multiple arguments.

To show help message below use `--help` argument.

```sh
usage: get-movies.py [--N <number>] | [--genres <list>] | [--year_from <year>] | [--year_to <year>] | [--regexp <regular-expression>] | [--help]

Select top n of the most rated movies.

options:
  --N           quantity of the most rated movies
  --genres      genres filter
  --year_from   start year filter
  --year_to     end year filter
  --regexp      regexp filter
  --help        show this help message and exit
```

All filters can be combined in any combination.

Output is always grouped by genre and sorted by rating DESC, year DESC, title ASC. 

## Examples

Set the working directory to `client/` and execute:

- Get all movies for each genre:
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

## Dependencies

- [mysql-connector-python](https://pypi.org/project/mysql/) - MySQL driver written in Python.

Libraries installation:
```
python -m pip install -r requirements.txt
```

## Configuration

Configuration file **config.ini** should be stored next to the script. It should contain sections:

#### [db]
- **database** — MySQL database name
- **host** — database host name 
- **user** — database user name
- **password** — database user password
- **proc_get_top_n_movies** — name of the MySQL stored procedure to call

## Requirements

Before utility using the source data should be load into the MySQL database.

Source csv-files should be downloaded from [grouplens.org](https://grouplens.org/datasets/movielens/):

- [MovieLens Latest Dataset (small)](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)
- [MovieLens Latest Dataset](https://files.grouplens.org/datasets/movielens/ml-latest.zip)
- [MovieLens 25M Dataset](https://files.grouplens.org/datasets/movielens/ml-25m.zip)

Example files included in the `server/landing/data/` directory.

### Download utility

Download utility can get source csv-files automatically. 

Usage:
```sh
setup.sh --ds small|medium|stable
```

## Landing

Landing script provides loading source csv-data into the MySQL database landing tables.

To load data set the working directory to `server/landing/` and execute:

```sh
> python landing.py
```
### Landing configuration

Configuration file **config.ini** should be stored next to the script. It should contain sections:

#### [db]
- **database** — MySQL database name
- **host** — database host name 
- **user** — database user name
- **password** — database user password

#### [Source]
- **movies_path** — input movies.csv filepath
- **ratings_path** — input ratings.csv filepath
- **encoding** — input files encoding
- **delimiter** — input files delimiter

#### [Destination]
- **movies_tbl** — name of the landing table for movies
- **ratings_tbl** — name of the landing table for ratings

#### [Settings]
- **chunk_size** — number of csv-rows to be loaded by single query

## Database

The utility use the MySQL database named `movielens`.

The database contains:

- `lnd_movies` — landing table for movies
- `lnd_ratings` — landing table for ratings
- `dst_movies` — destination table
- `proc_get_top_n_movies` — stored procedure to be called by client
