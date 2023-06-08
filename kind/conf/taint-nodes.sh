#!/bin/bash

kubectl taint nodes wikimedia-worker platform=kafka:NoSchedule
kubectl taint nodes wikimedia-worker2 platform=kafka:NoSchedule
kubectl taint nodes wikimedia-worker3 platform=kafka:NoSchedule
kubectl taint nodes wikimedia-worker4 platform=spark:NoSchedule
kubectl taint nodes wikimedia-worker5 platform=spark:NoSchedule
kubectl taint nodes wikimedia-worker6 platform=spark:NoSchedule
kubectl taint nodes wikimedia-worker7 platform=spark:NoSchedule
kubectl taint nodes wikimedia-worker8 platform=database:NoSchedule
kubectl taint nodes wikimedia-worker9 platform=superset:NoSchedule