# CivicPulse

CivicPulse is a smart complaint management platform that uses AI to automatically categorize and prioritize civic issues (like potholes, broken streetlights, or waste management).

## Getting Started

The easiest way to run the entire stack locally is using Docker Compose.

### Prerequisites
- Docker & Docker Desktop
- Node.js (for local frontend development)
- Python 3.11+ (for local backend development)

### Running with Docker Compose (Recommended)
This spins up the frontend, backend, PostgreSQL database, and Redis cache automatically.

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

Once running, access the app:
- **Frontend**: http://localhost:5173
- **Backend API Docs (Swagger)**: http://localhost:8000/docs

### Architecture Overview
- **Frontend**: React, Vite, TypeScript, Vitest
- **Backend**: FastAPI, SQLAlchemy, Alembic, Pytest
- **Database**: PostgreSQL 16
- **Cache / Rate Limiting**: Redis 7
- **AI Triage**: Groq (Llama3) with rule-based fallback
- **Container Orchestration**: Kubernetes (via k3d locally)

For troubleshooting and Kubernetes deployment, please refer to the [Runbook](docs/RUNBOOK.md).
