# Get-movies

Pure python utility to get top n movies by each genre from csv data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source filepaths specified in the script.


## Options

All options are optional.

- **--N** *<n>* — number filter, limit movies count for output
- **--genres** *<genres list>* — genres filter, list of genres separated by '|'
- **--year_from** *<year>* — year-from filter
- **--year_to** *<year>* — year-to filter
- **--regexp** *<regexp>* — regexp filter for title
- **--help** — show this help message and exit

## Usage/Examples

```
get-movies.py [--N <number>] | [--genres <list>] | [--year_from <year>] | [--year_to <year>] | [--regexp <regular-expression>] | [--help]
```
All filters can be combined in any combination.
Output is always grouped by genre and sorted by rating DESC, year DESC, title ASC. 

Get all movies for each genre:
```
get-movies.py

genre,title,year,rating
Action,Tokyo Tribe,2014,5.0
Action,Justice League: Doom,2012,5.0
Action,On the Other Side of the Tracks (De l'autre côté du périph),2012,5.0
Action,Faster,2010,5.0
Action,Superman/Batman: Public Enemies,2009,5.0
...
```

Get all movies for both "Sci-Fi" and "War" genres:
```
get-movies.py --genres "Sci-Fi|War"

genre,title,year,rating
Sci-Fi,SORI: Voice from the Heart,2016,5.0
Sci-Fi,The Girl with All the Gifts,2016,5.0
Sci-Fi,Delirium,2014,5.0
...
War,Battle For Sevastopol,2015,5.0
War,Che: Part One,2008,5.0
War,Che: Part Two,2008,5.0
...
```

Get 3 top rated movies for both "Sci-Fi" and "War" genres:
```
get-movies.py --N 3 --genres "Sci-Fi|War"

genre,title,year,rating
Sci-Fi,SORI: Voice from the Heart,2016,5.0
Sci-Fi,The Girl with All the Gifts,2016,5.0
Sci-Fi,Delirium,2014,5.0
War,Battle For Sevastopol,2015,5.0
War,Che: Part One,2008,5.0
War,Che: Part Two,2008,5.0
```

Get all movies released from 1990 to 2000 for "War" genre:
```
get-movies.py --year_from 1990 --year_to 2000 --genre "War"

genre,title,year,rating
War,Train of Life (Train de vie),1998,4.5
War,"Colonel Chabert, Le",1994,4.5
War,Underground,1995,4.333333333333333
War,Europa Europa (Hitlerjunge Salomon),1990,4.333333333333333
War,Joint Security Area (Gongdong gyeongbi guyeok JSA),2000,4.25
...
```

Get 3 top rated movies with title containing "the" or "The" for "Sci-Fi" genre:
```
get-movies.py --N 3 --regexp ".[Tt]he " --genre "Sci-Fi"

genre,title,year,rating
Sci-Fi,SORI: Voice from the Heart,2016,5.0
Sci-Fi,The Girl with All the Gifts,2016,5.0
Sci-Fi,"Mystery of the Third Planet, The (Tayna tretey planety)",1981,5.0
...
```

Show help message:
```
convert.py --help
```

## Requirements

Source files should be downloaded from [grouplens.org](https://grouplens.org/datasets/movielens/):

- [MovieLens Latest Dataset (small)](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)
- [MovieLens Latest Dataset](https://files.grouplens.org/datasets/movielens/ml-latest.zip)
or
- [MovieLens 25M Dataset](https://files.grouplens.org/datasets/movielens/ml-25m.zip)
