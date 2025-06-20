#!/bin/bash

CONTAINER_NAME="wikiwar_solr"
COLLECTION_NAME="wikiwar"
DATA_FILE="output.json"

# Verify if the container is already running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then  
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Run the Solr container
docker run -p 8983:8983 --name $CONTAINER_NAME -v "$(pwd):/data" -d solr:9 solr-precreate $COLLECTION_NAME

sleep 5

#Without schema configuration

#Populate the collection
docker exec $CONTAINER_NAME bin/solr post -c $COLLECTION_NAME /data/$DATA_FILE
