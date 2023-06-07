#!/bin/bash

set -euo pipefail

BASE_DIR="$(pwd)"
REPO_DIR="${BASE_DIR}/.."

(
cd ${REPO_DIR}

# Application on Kubernetes 

# Create kind cluster on kubernetes
kind create cluster --name wiki-cluster \
--image kindest/node:v1.27.0 \
--config kind/conf/cluster-config.yaml

# Taint nodes on wiki cluster
kubectl taint nodes wiki-cluster-worker platform=airflow:NoSchedule
kubectl taint nodes wiki-cluster-worker2 platform=spark:NoSchedule
kubectl taint nodes wiki-cluster-worker3 platform=spark:NoSchedule
kubectl taint nodes wiki-cluster-worker4 platform=spark:NoSchedule
kubectl taint nodes wiki-cluster-worker5 platform=spark:NoSchedule
kubectl taint nodes wiki-cluster-worker6 platform=trino:NoSchedule
kubectl taint nodes wiki-cluster-worker7 platform=trino:NoSchedule
kubectl taint nodes wiki-cluster-worker8 platform=trino:NoSchedule
kubectl taint nodes wiki-cluster-worker9 platform=trino:NoSchedule

# Apache Airflow
kubectl create ns airflow

# Extending airflow image
# build the airflow extended image
docker build --no-cache --tag airflow-image:0.0.1 kubernetes/airflow/.

# Load the airflow extended image into kind
kind load docker-image airflow-image:0.0.1 -n wiki-cluster

# Create the secret for using gitsync
kubectl create secret generic airflow-ssh-secret \
--from-file=gitSshKey=/Users/yjkim-studio/.ssh/id_rsa \
-n airflow

# Install airflow Helm
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm search repo airflow
helm install -f kubernetes/airflow/conf/values.yaml airflow apache-airflow/airflow \
--namespace airflow \
--set images.airflow.repository=airflow-image \
--set images.airflow.tag=0.0.1

# Apply apache airflow variables
kubectl apply -f kubernetes/airflow/conf/variables.yaml

# Execute the apache airflow webserver
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow \
--context kind-wiki-cluster

# Trino
kubectl create ns trino
helm repo add trino https://trinodb.github.io/charts
helm install -f kubernetes/trino/conf/values.yaml trino trino/trino \
--namespace trino

# Apache Spark
kubectl create ns spark

# Application on Docker

# Apache Supserset
docker-compose --project-name=superset -f docker/superset/docker-compose.yaml pull
docker-compose --project-name=superset -f docker/superset/docker-compose.yaml up

# Minio
# Create networks for minio
docker network create --gateway 172.28.0.1 --subnet 172.28.0.0/21 hive-metastore

# Launch minio 
docker-compose --project-name=hive-metastore -f docker/minio/docker-compose.yaml up

# Postgresql
# Create networks for Postgresql
docker network create --gateway 172.24.0.1 --subnet 172.24.0.0/21 postgres

docker pull postgres:14.8
docker run --name postgres \
--network postgres \
--ip 172.24.0.4 \
-p 5432:5432 \
-e POSTGRES_PASSWORD=postgres \
-v "${REPO_DIR}/docker/postgresql/data":/var/lib/postgresql/data \
-d postgres:14.8

# Create a database
docker exec postgres sh -c "psql -U postgres -c 'create database trino;'"

# Connect the networks 
# connect hive metastore to trino
docker network connect kind hive-metastore
docker network connect kind minio
docker network connect kind mysql

# connect postgresql to trino
docker network connect kind postgres
docker network connect postgres wiki-cluster-worker2
docker network connect postgres wiki-cluster-worker3
docker network connect postgres wiki-cluster-worker4
docker network connect postgres wiki-cluster-worker5
docker network connect postgres wiki-cluster-worker6
docker network connect postgres wiki-cluster-worker7
docker network connect postgres wiki-cluster-worker8
docker network connect postgres wiki-cluster-worker9
)