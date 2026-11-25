set -eu
. ./deploy/oauth-state.sh
set -e
if [ -z "${BUILD_NUMBER}" ]; then
  echo "BUILD_NUMBER is required"
  exit 1
fi
sed 's/${TAG}/'"$BUILD_NUMBER"'/g' deploy/production/deployment.yaml | kubectl apply -f -
mark_oauth_key_initialized
kubectl apply -f deploy/production/service.yaml
kubectl apply -f deploy/production/ingress.yaml
