# CivicPulse Runbook

This document contains operational procedures, troubleshooting steps, and engineering notes for maintaining CivicPulse.

## 1. Local Development (Docker Compose)

### Rebuilding Containers
If you change `Dockerfile` or install new Python/npm dependencies:
```bash
docker compose up -d --build
```

### Database Migrations
Always use Alembic to manage database schema changes.
```bash
# Generate a new migration
docker compose exec backend alembic revision --autogenerate -m "Migration description"

# Apply migrations
docker compose exec backend alembic upgrade head
```

### Viewing Logs
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

## 2. Kubernetes Deployment (k3d)

### Initial Setup
Ensure `k3d` and `kubectl` are installed.
```bash
k3d cluster create civicpulse -p "8080:80@loadbalancer"
```

### Loading Images
If you update the code, build and load it into k3d:
```bash
docker compose build
docker tag civicpulse-backend:latest civicpulse-backend:dev
docker tag civicpulse-frontend:latest civicpulse-frontend:dev
k3d image import civicpulse-backend:dev civicpulse-frontend:dev -c civicpulse
```

### Managing Secrets
Secrets are passed via `.env` but stored securely in Kubernetes.
```bash
kubectl create secret generic civicpulse-secrets --from-env-file=.env -n civicpulse
```

### Troubleshooting Kubernetes
If pods are crashing, investigate with:
```bash
# Check pod statuses
kubectl get pods -n civicpulse

# Describe a crashing pod to see why it failed
kubectl describe pod <pod-name> -n civicpulse

# View logs for a pod
kubectl logs <pod-name> -n civicpulse
```

## 3. Disaster Recovery

**Database Data Loss**:
- If `postgres_data` volume is deleted, records will be lost.
- To re-seed dummy data for testing: `docker compose exec backend python seed.py`

**AI Triage Failure**:
- If Groq goes down or API limits are reached, the system automatically falls back to a rule-based regex engine. No manual intervention is needed. To test this, provide an invalid API key and submit a complaint.
