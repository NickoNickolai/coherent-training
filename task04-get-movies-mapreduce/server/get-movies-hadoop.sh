#!/bin/bash

args=$1

export DIR=/root

hdfs dfs -mkdir /task04
hdfs dfs -put $DIR/movies.csv /task04

yarn jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
     -input /task04/movies.csv \
     -output /task04/output \
     -file $DIR/mapper.py $DIR/reducer.py \
     -mapper "python mapper.py '$args'" \
     -reducer "python reducer.py '$args'"

hdfs dfs -get /task04/output $DIR

hdfs dfs -rm -r /task04/output

cat $DIR/output/part-00000

rm -r $DIR/output
