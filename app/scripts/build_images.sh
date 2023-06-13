#!/bin/bash

# Python scripts for ingesting wiki pageview 
docker build --tag ingest-wiki:0.0.1 ingest_wiki/.
kind load docker-image ingest-wiki:0.0.1 --name wiki-cluster

# Python scripts for converting wiki pageview 
docker build --tag convert-wiki:0.0.1 convert_wiki/.
kind load docker-image convert-wiki:0.0.1 --name wiki-cluster

# Python scripts for wrangling wiki pageview 
docker build --tag wrangling-wiki:0.0.1 wrangling_wiki/.
kind load docker-image wrangling-wiki:0.0.1 --name wiki-cluster