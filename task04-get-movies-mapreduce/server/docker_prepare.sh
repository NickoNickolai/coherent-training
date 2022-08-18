CONTAINER=cloudera_quickstart
DIR=/root

sudo docker exec $CONTAINER rm $DIR/movies.csv
sudo docker exec $CONTAINER rm $DIR/mapper.py
sudo docker exec $CONTAINER rm $DIR/reducer.py
sudo docker exec $CONTAINER rm $DIR/get-movies-local.sh
sudo docker exec $CONTAINER rm $DIR/get-movies-hadoop.sh

sudo docker cp data/movies.csv $CONTAINER:$DIR
sudo docker cp mapper.py $CONTAINER:$DIR
sudo docker cp reducer.py $CONTAINER:$DIR
sudo docker cp get-movies-local.sh $CONTAINER:$DIR
sudo docker cp get-movies-hadoop.sh $CONTAINER:$DIR
