use movielens;

create table if not exists lnd_ratings(
    id int not null primary key auto_increment,
    movieId varchar(255),
    rating varchar(255)
);