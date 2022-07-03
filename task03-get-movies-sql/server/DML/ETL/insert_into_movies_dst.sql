use movielens;

truncate dst_movies;

insert into dst_movies (movieId, title, year, genre, rating)
with
cte_calc_avg_rating as (
	select
		m.movieId,
        m.title,
        m.genres,
        avg(r.rating) as rating
	from
		lnd_movies m 
        join lnd_ratings r on r.movieId = m.movieId
	group by
		r.movieId
),
cte_split_title as (
	select
		movieId,
        regexp_substr(trim(title), '.*(?= \\([0-9]{4}\\))') as title,
        regexp_substr(trim(title), '(?=[0-9]{4}\\))[0-9]{4}') as year,
        genres,
        rating
	from
		cte_calc_avg_rating
),
cte_split_genres as (
	select
		m.movieId,
        m.title,
        convert(m.year, unsigned) as year,
        g.genre as genre,
        m.rating
	from
		cte_split_title m
        join json_table(
			replace(json_array(trim(m.genres)), '|', '","'),
            '$[*]' columns (genre varchar(30) path '$')
        ) g
	where
		m.genres != '(no genres listed)' and (m.title is not null or m.year is not null)
)
select
	movieId,
    title,
    year,
    genre,
    rating
from
	cte_split_genres;