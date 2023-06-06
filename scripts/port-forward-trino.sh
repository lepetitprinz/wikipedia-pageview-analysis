#!/bin/bash

POD_NAME=$(kubectl get pods -n trino -l "app=trino,release=trino,component=coordinator" -o name)
kubectl -n trino port-forward $POD_NAME 8000:8000