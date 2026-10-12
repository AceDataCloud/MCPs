set -eu

# Keep the OAuth state store password stable across deployments.
if ! kubectl -n acedatacloud get secret mcp-acedatacloud-oauth-redis >/dev/null 2>&1; then
  if kubectl -n acedatacloud get pvc data-mcp-acedatacloud-oauth-redis-0 >/dev/null 2>&1; then
    echo "OAuth state key is missing; restore the existing Secret before deployment" >&2
    exit 1
  fi
  oauth_redis_password=$(openssl rand -hex 32)
  oauth_state_key=$(openssl rand -hex 32)
  kubectl -n acedatacloud create secret generic mcp-acedatacloud-oauth-redis \
    --from-literal=password="$oauth_redis_password" \
    --from-literal=state_key="$oauth_state_key" >/dev/null
  unset oauth_redis_password oauth_state_key
fi
oauth_secret_ready=$(kubectl -n acedatacloud get secret mcp-acedatacloud-oauth-redis \
  -o go-template='{{if and (index .data "password") (index .data "state_key")}}yes{{end}}')
if [ "$oauth_secret_ready" != yes ]; then
  echo "OAuth state Secret must contain password and state_key" >&2
  exit 1
fi

kubectl apply -f deploy/production/oauth-redis.yaml
kubectl -n acedatacloud rollout status statefulset/mcp-acedatacloud-oauth-redis --timeout=600s
sed 's/\${TAG}/'"$BUILD_NUMBER"'/g' deploy/production/deployment.yaml | kubectl apply -f -
kubectl apply -f deploy/production/service.yaml
kubectl apply -f deploy/production/ingress.yaml
kubectl -n acedatacloud rollout status deployment/mcp-acedatacloud --timeout=600s
