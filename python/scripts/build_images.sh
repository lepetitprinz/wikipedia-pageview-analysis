#!/bin/bash

# Python scripts for ingesting wiki pageview 
docker build --tag ingest-wiki:0.0.1 ingest_wiki/.
kind load docker-image ingest-wiki:0.0.1 --name wiki-cluster

# Python scripts for sinking wiki pageview 
docker build --tag sink-wiki:0.0.1 sink_wiki/.
kind load docker-image sink-wiki:0.0.1 --name wiki-cluster