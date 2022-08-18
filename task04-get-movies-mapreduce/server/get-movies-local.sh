#!/bin/bash

args=$1

export DIR=/root

cat $DIR/movies.csv |
python $DIR/mapper.py "$args" |
sort |
python $DIR/reducer.py "$args"

read
