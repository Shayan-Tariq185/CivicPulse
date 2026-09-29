docker compose build frontend
docker tag civicpulse-frontend civicpulse-frontend:dev
k3d image import civicpulse-frontend:dev -c civicpulse
kubectl delete pods -l app=frontend -n civicpulse
kubectl get pods -n civicpulse -w
