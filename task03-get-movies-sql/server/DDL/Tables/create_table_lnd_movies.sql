use movielens;

drop table if exists lnd_movies;

create table lnd_movies(
    id int not null primary key auto_increment,
    movieId varchar(255),
    title varchar(255),
    genres varchar(255)
);
