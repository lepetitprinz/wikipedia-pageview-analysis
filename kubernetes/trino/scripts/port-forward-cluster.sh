#!/bin/bash

POD_NAME=$(kubectl get pods -n trino -l "app=trino,release=trino-cluster,component=coordinator" -o name)

kubectl -n trino port-forward $POD_NAME 8080:8080