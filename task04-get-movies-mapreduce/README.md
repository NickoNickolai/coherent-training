# Get-movies (Hadoop Streaming)

Python/Hadoop-streaming utility to get top n movies by each genre from csv data.
Outputs to the stdout in csv-like format: (genre, title, year, rating).
Source files should be uploaded into HDFS.

## Requirements

The utility requires:
- [**`python3`**](https://www.python.org/downloads/) interpreter with [**`pip`**](https://pypi.org/project/pip/) installing tool
- Linux OS (Ubuntu) with [**`docker`**](https://www.docker.com)

On the command line the interpreter can be typed as `python`, `python3`, `py` (depending on OS, version, etc.).

To be specific this readme has decided to use the interpreter name `python` in the examples.

## Usage

All options are optional. To show help message below use `--help` option.

```sh
usage: get-movies.py [--N <number>] [--genres <list>] [--year_from <year>] [--year_to <year>] [--regexp <regexp>] [--help]

Python/Hadoop-streaming utility to get top n movies by each genre from csv data. Outputs to the stdout in csv-like
format: (genre, title, year, rating). Source files should be uploaded into HDFS.

options:
  --N <number>        top rated movies count for each genre
  --genres <list>     genres filter, list separated by '|'
  --year_from <year>  year-from filter
  --year_to <year>    year-to filter
  --regexp <regexp>   regexp filter for title
  --help              show this help message and exit
```

All filters can be combined in any combination.
Output is always grouped by genre and sorted by year DESC, title ASC. 

## Examples

- Get all movies for each genre
```sh
> python get-movies.py

...  
Action,Ant-Man and the Wasp,2018	
Action,Avengers: Infinity War - Part I,2018	
Action,Bungo Stray Dogs: Dead Apple,2018	
Action,Deadpool 2,2018	
Action,Death Wish,2018
...
```

- Get 3 top movies for both "Sci-Fi" and "War" genres:
```sh
> python get-movies.py --N 3 --genres "Sci-Fi|War"

... 
Sci-Fi,Space Truckers,1996
Sci-Fi,Frankenstein Unbound,1990
Sci-Fi,Death Race 2000,1975
War,Darkest Hour,2017
War,Dunkirk,2017
War,Valhalla Rising,2009
```

- Get 3 top movies with title containing "the" or "The" for "Sci-Fi" genre released from 1999 to 2000 year:
```sh
> python get-movies.py --N 3 --regexp ".[Tt]he " --genre "Sci-Fi" --year_from 1999 --year_to 2000

...
Sci-Fi,Batman Beyond: Return of the Joker,2000
Sci-Fi,Star Wars: Episode I - The Phantom Menace,1999
Sci-Fi,Universal Soldier: The Return,1999
```

## Configuration

Configuration file `config.ini` should be stored next to the script. It should contain:

**[Source]**

- `delimiter` — input file delimiter

**[Destination]**

- `delimiter` — output data delimiter

**[Extraction]**

- `title_regexp` — regular expression to split raw title into the real title and year
- `no_genres_regexp` — regular expression to detect movies with no genre

**[Extraction]**

- `executor` — execution bash script filepath

## Hadoop

The utility requires docker container [`cloudera/quickstart`](https://hub.docker.com/r/cloudera/quickstart).

To run docker container execute `docker_create.sh` from `server/` directory:
```
> docker_create.sh
```

To prepare docker container with server-side sources execute `docker_prepare.sh` from `server/` directory:
```
> docker_prepare.sh
```

Execution scripts for config-file:

- `/root/get-movies-local.sh` for the hadoop emulation
- `/root/get-movies-hadoop.sh` for the real hadoop

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
