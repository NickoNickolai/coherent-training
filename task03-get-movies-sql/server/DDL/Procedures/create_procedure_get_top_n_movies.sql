use movielens;

delimiter $$
create procedure if not exists get_top_n_movies(
	in N int,
    in genres varchar(255),
    in year_from int,
    in year_to int,
    in regex varchar(255)
)
begin
	if genres is null then
		set genres =  '|';
	end if;
    
    set genres = concat(genres, '|');
    
	while genres != '' do
    
		select 
			genre, title, year, rating
		from
			dst_movies
		where
			if(regex is null, true, title regexp regex) and
            if(genres = '|', true, genre = left(genres, locate('|', genres) - 1)) and
            if(year_from is null, true, year >= year_from) and
            if(year_to is null, true, year <= year_to)
		order by
			genre asc, rating desc, year desc, title asc
		limit n;

		set genres = replace(genres, left(genres, locate('|', genres)), '');
	end while;
end; 
$$