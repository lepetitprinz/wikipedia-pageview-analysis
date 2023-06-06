#! /bin/bash

docker network create --gateway 172.28.0.1 --subnet 172.28.0.0/16 hive-metastore

docker-compose build
docker-compose --project-name=hive-metastore up -d