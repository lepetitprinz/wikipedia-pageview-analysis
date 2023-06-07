#!/bin/bash
kubectl create secret generic airflow-ssh-secret \
--from-file=gitSshKey=/Users/yjkim-studio/.ssh/id_rsa -n airflow