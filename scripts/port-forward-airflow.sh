#!/bin/bash
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow --context kind-wiki-cluster