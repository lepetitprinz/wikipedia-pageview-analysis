#!/bin/bash

# build the airflow extended image
docker build --no-cache --tag airflow-image:0.0.1 .

# Load the airflow extended image into kind
kind load docker-image airflow-image:0.0.1 -n wiki-cluster

# Upgrade airflow helm chart
helm upgrade --install -f conf/values.yaml airflow apache-airflow/airflow \
--namespace airflow \
--set images.airflow.repository=airflow-image \
--set images.airflow.tag=0.0.1