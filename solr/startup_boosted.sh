#!/bin/bash

CONTAINER_NAME="wikiwar_solr"
COLLECTION_NAME="wikiwar"
DATA_FILE="output.json"
SCHEMA_FILE="schema_boosted.json"

# Verify if there is a container with the same name
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then  
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Run the Solr container
docker run -p 8983:8983 --name $CONTAINER_NAME -v "$(pwd):/data" \
    -e SOLR_OPTS="-Dsolr.enable.cors=true \
                  -Dsolr.cors.allow-origin='*' \
                  -Dsolr.cors.allow-methods='GET,POST,OPTIONS' \
                  -Dsolr.cors.allow-headers='Content-Type,Authorization'" \
    -d solr:9 solr-precreate $COLLECTION_NAME

sleep 5

#Schema configuration - Boosted schema
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@$SCHEMA_FILE" \
    http://localhost:8983/solr/$COLLECTION_NAME/schema


#Populate the collection
docker exec $CONTAINER_NAME bin/solr post -c $COLLECTION_NAME /data/$DATA_FILE
