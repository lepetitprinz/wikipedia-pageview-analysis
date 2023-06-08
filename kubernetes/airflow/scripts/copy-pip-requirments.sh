#!/bin/bash

cd ~
BASE_DIR="$(pwd)"
FROM_DIR="${BASE_DIR}/venv/airflow/requirements.txt"
TO_DIR="${BASE_DIR}/src/project/wikipedia-pageview-analysis/kubernetes/airflow/requirements.txt"

cp $FROM_DIR $TO_DIR