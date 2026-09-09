set -eu

DEPLOYMENT_NAME=$(awk '$1 == "name:" { print $2; exit }' deploy/production/deployment.yaml)
NAMESPACE=$(awk '$1 == "namespace:" { print $2; exit }' deploy/production/deployment.yaml)

sed 's/\${TAG}/'"$BUILD_NUMBER"'/g' deploy/production/deployment.yaml | kubectl apply -f -
kubectl apply -f deploy/production/service.yaml
kubectl apply -f deploy/production/ingress.yaml
kubectl rollout status "deployment/$DEPLOYMENT_NAME" --namespace "$NAMESPACE" --timeout=300s
