use movielens;

drop table if exists lnd_ratings;

create table lnd_ratings(
    id int not null primary key auto_increment,
    movieId varchar(255),
    rating varchar(255)
);
