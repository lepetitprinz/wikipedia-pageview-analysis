#!/bin/bash

kind create cluster --name trino --config conf/trino-kind-config.yaml --image kindest/node:v1.27.0

kubectl create ns trino
kubectl taint nodes trino-worker platform=trino:NoSchedule
kubectl taint nodes trino-worker2 platform=trino:NoSchedule
kubectl taint nodes trino-worker3 platform=trino:NoSchedule

helm repo add trino https://trinodb.github.io/charts

helm install -f conf/config-with-catalogs.yaml trino-cluster trino/trino \
--namespace trino --create-namespace