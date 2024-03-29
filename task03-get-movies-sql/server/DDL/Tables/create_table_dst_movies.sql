use movielens;

drop table if exists dst_movies;

create table dst_movies(
    id int not null primary key auto_increment,
    movieId int not null,
    title varchar(255) not null,
    year int not null,
    genre varchar(30) not null,
    rating float not null
);
