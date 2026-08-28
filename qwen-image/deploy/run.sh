#!/bin/sh
set -eu

: "${BUILD_NUMBER:?BUILD_NUMBER is required}"

rendered=$(mktemp)
trap 'rm -f "$rendered"' EXIT
sed 's/${TAG}/'"$BUILD_NUMBER"'/g' deploy/production/deployment.yaml > "$rendered"
deployment=$(kubectl apply -f "$rendered" -o name)
kubectl apply -f deploy/production/service.yaml
kubectl apply -f deploy/production/ingress.yaml
kubectl -n acedatacloud rollout status "$deployment" --timeout=15m
