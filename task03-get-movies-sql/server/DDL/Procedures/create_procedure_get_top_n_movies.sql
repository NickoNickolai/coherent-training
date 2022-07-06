use movielens;

drop procedure if exists get_top_n_movies;

delimiter $$
create procedure get_top_n_movies(
	in N int,
    in genres varchar(255),
    in year_from int,
    in year_to int,
    in regex varchar(255)
)
begin
	set @genres_delimiter = '|';
	set @max_int = 2147483647;

	if N is null then
		set N = @max_int;
	end if;
        
	if genres is null then
		set genres =  '';
	end if;
    
    set genres = concat(genres, @genres_delimiter);
    
	while genres != '' do
    
		select 
			genre, title, year, rating
		from
			dst_movies
		where
			if(regex is null, true, regexp_like(title, regex, 'c')) and
            if(genres = @genres_delimiter, true, genre = left(genres, locate(@genres_delimiter, genres) - 1)) and
            if(year_from is null, true, year >= year_from) and
            if(year_to is null, true, year <= year_to)
		order by
			binary genre asc, rating desc, year desc, binary title asc
		limit N;

		set genres = replace(genres, left(genres, locate(@genres_delimiter, genres)), '');
	end while;
end; 
$$
