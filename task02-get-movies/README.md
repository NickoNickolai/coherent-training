# Get-movies

Pure python utility to get top n movies by each genre from csv-data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source filepaths specified in config file.


## Options

All options are optional.

- **--N** *<n>* — number filter, limit movies count for output
- **--genres** *<genres list>* — genres filter, list of genres separated by '|'
- **--year_from** *<year>* — year-from filter
- **--year_to** *<year>* — year-to filter
- **--regexp** *<regexp>* — regexp filter for title
- **--help** — show this help message and exit

## Usage

```sh
get-movies.py [--N <number>] | [--genres <list>] | [--year_from <year>] | [--year_to <year>] | [--regexp <regular-expression>] | [--help]
```

All filters can be combined in any combination.
Output is always grouped by genre and sorted by rating DESC, year DESC, title ASC. 

## Examples

Get all movies for each genre:
```sh
get-movies.py

genre,title,year,rating
Action,Tokyo Tribe,2014,5.0
Action,Justice League: Doom,2012,5.0
Action,On the Other Side of the Tracks (De l'autre côté du périph),2012,5.0
Action,Faster,2010,5.0
Action,Superman/Batman: Public Enemies,2009,5.0
...
```

Get 3 top rated movies for both "Sci-Fi" and "War" genres:
```sh
get-movies.py --N 3 --genres "Sci-Fi|War"

genre,title,year,rating
Sci-Fi,SORI: Voice from the Heart,2016,5.0
Sci-Fi,The Girl with All the Gifts,2016,5.0
Sci-Fi,Delirium,2014,5.0
War,Battle For Sevastopol,2015,5.0
War,Che: Part One,2008,5.0
War,Che: Part Two,2008,5.0
```

Get 3 top rated movies with title containing "the" or "The" for "Sci-Fi" genre released from 1999 to 2000 year:
```sh
get-movies.py --N 3 --regexp ".[Tt]he " --genre "Sci-Fi" --year_from 1999 --year_to 2000

genre,title,year,rating
Sci-Fi,Batman Beyond: Return of the Joker,2000,3.5
Sci-Fi,Star Wars: Episode I - The Phantom Menace,1999,3.107142857142857
Sci-Fi,Universal Soldier: The Return,1999,2.625
```

Show help message:
```sh
convert.py --help
```

## Configuration

Configuration file **config.ini** should be stored next to the script. It should contain:

#### [Source]
- **movies_path** — input movies.csv filepath
- **ratings_path** — input ratings.csv filepath
- **encoding** — input files encoding
- **delimiter** — input files delimiter
#### [Destination]
- **encoding** — output data encoding
- **delimiter** — output data delimiter
- **write_schema** — enable output schema 
#### [Settings]
- **title_regexp** — regular expression to split raw title into the real title and year
- **no_genres_regexp** — regular expression to detect movies with no genre

## Requirements

Source files should be downloaded from [grouplens.org](https://grouplens.org/datasets/movielens/):

- [MovieLens Latest Dataset (small)](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)
- [MovieLens Latest Dataset](https://files.grouplens.org/datasets/movielens/ml-latest.zip)
- [MovieLens 25M Dataset](https://files.grouplens.org/datasets/movielens/ml-25m.zip)

Example files included in the **data/** directory.

### Download utility

Usage of the additional shell utilitiy to automatically download source files:
```sh
setup.sh --ds small|medium|stable
```
