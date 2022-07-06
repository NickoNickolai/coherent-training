use movielens;

set @title_regexp = '.*(?= \\([0-9]{4}\\)+$)';
set @year_regexp = '(?=[0-9]{4}\\)+$)[0-9]{4}';
set @genres_delimiter = '|';
set @no_genres_placeholder = '(no genres listed)';

truncate dst_movies;

insert into dst_movies (movieId, title, year, genre, rating)
with 
cte_movies_with_rating as ( 
	select 
		m.movieId, 
        m.title, 
        m.genres, 
        avg(r.rating) as rating 
	from 
		lnd_movies m  
	join 
		lnd_ratings r on r.movieId = m.movieId 
	group by 
		m.movieId, 
        m.title, 
        m.genres 
), 
cte_movies_with_title_year as ( 
	select 
		movieId, 
        regexp_substr(trim(title), @title_regexp) as title, 
        regexp_substr(trim(title), @year_regexp) as year, 
        genres, 
        rating 
	from 
		cte_movies_with_rating 
), 
cte_movies_with_genre as ( 
	select 
		m.movieId, 
        m.title, 
        convert(m.year, unsigned) as year, 
        g.genre as genre, 
        m.rating 
	from 
		cte_movies_with_title_year m 
	join 
		json_table( 
			replace(json_array(trim(m.genres)), @genres_delimiter, '","'), 
            '$[*]' columns (genre varchar(30) path '$') 
        ) g 
	where 
		m.genres != @no_genres_placeholder and 
		m.title is not null and 
		m.year is not null 
) 
select 
	movieId, 
    title, 
    year, 
    genre, 
    rating 
from 
	cte_movies_with_genre;
