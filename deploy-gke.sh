#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
PROJECT_ID="project-6b07c7a3-5303-403d-bf7"
CLUSTER_NAME="evolution-of-todo"
REGION="us-central1"
AR_HOST="${REGION}-docker.pkg.dev/${PROJECT_ID}/todo-app"
RELEASE_NAME="todo-app"
TAG="${1:-latest}"

echo "==> Phase V: Deploying to GKE"
echo "    Project:  ${PROJECT_ID}"
echo "    Cluster:  ${CLUSTER_NAME}"
echo "    Region:   ${REGION}"
echo "    Tag:      ${TAG}"

# --- 1. Authenticate with GKE cluster ---
echo ""
echo "==> Authenticating with GKE cluster..."
gcloud container clusters get-credentials "${CLUSTER_NAME}" --region "${REGION}" --project "${PROJECT_ID}"

# --- 2. Build Docker images ---
echo ""
echo "==> Building backend image..."
docker build -t "${AR_HOST}/todo-backend:${TAG}" ./backend

echo ""
echo "==> Building frontend image..."
docker build -t "${AR_HOST}/todo-frontend:${TAG}" \
  --build-arg NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8000}" \
  ./frontend

# --- 3. Push images to Artifact Registry ---
echo ""
echo "==> Configuring Docker for Artifact Registry..."
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

echo "==> Pushing backend image..."
docker push "${AR_HOST}/todo-backend:${TAG}"

echo "==> Pushing frontend image..."
docker push "${AR_HOST}/todo-frontend:${TAG}"

# --- 4. Create Kubernetes secrets from .env ---
echo ""
echo "==> Creating Kubernetes secrets from .env..."
if [ ! -f .env ]; then
  echo "ERROR: .env file not found in project root"
  exit 1
fi

# Delete existing secret if it exists, then recreate
kubectl delete secret "${RELEASE_NAME}-secrets" --ignore-not-found

kubectl create secret generic "${RELEASE_NAME}-secrets" \
  --from-env-file=.env \
  --dry-run=client -o yaml | kubectl apply -f -

# --- 5. Deploy with Helm ---
echo ""
echo "==> Deploying with Helm..."
helm upgrade --install "${RELEASE_NAME}" ./helm \
  --set backend.tag="${TAG}" \
  --set frontend.tag="${TAG}"

# --- 6. Wait for rollout ---
echo ""
echo "==> Waiting for backend rollout..."
kubectl rollout status deployment/"${RELEASE_NAME}-backend" --timeout=120s

echo "==> Waiting for frontend rollout..."
kubectl rollout status deployment/"${RELEASE_NAME}-frontend" --timeout=120s

# --- 7. Print service info ---
echo ""
echo "==> Deployment complete! Service info:"
kubectl get svc "${RELEASE_NAME}-frontend" "${RELEASE_NAME}-backend"
echo ""
echo "Note: LoadBalancer external IPs may take a minute to provision."
echo "Run 'kubectl get svc -w' to watch for EXTERNAL-IP assignment."
