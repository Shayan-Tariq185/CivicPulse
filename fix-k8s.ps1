docker compose down

echo "Building and tagging images..."
docker compose build
docker tag civicpulse-backend civicpulse-backend:dev
docker tag civicpulse-frontend civicpulse-frontend:dev

echo "Importing images into k3d..."
k3d image import civicpulse-backend:dev civicpulse-frontend:dev -c civicpulse

echo "Creating secrets from .env..."
kubectl create secret generic civicpulse-secrets --from-env-file=.env -n civicpulse --dry-run=client -o yaml | kubectl apply -f -

echo "Applying Kubernetes manifests..."
kubectl apply -k k8s/overlays/dev

echo "Waiting for pods to be ready (press Ctrl+C when all are Running)..."
kubectl get pods -n civicpulse -w
