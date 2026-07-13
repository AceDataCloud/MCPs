#!/bin/sh
set -eu

sed 's/${TAG}/'"$BUILD_NUMBER"'/g' deploy/production/deployment.yaml | kubectl apply -f -
kubectl apply -f deploy/production/service.yaml
kubectl apply -f deploy/production/ingress.yaml