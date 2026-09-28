from fastapi import APIRouter, Response, status
from sqlalchemy import text

from database import engine
from metrics import prometheus_text
from redis_client import check_redis_health

router = APIRouter(tags=["operations"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def ready(response: Response) -> dict[str, object]:
    postgres_ok = False
    redis_ok = False

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        postgres_ok = True
    except Exception:  # noqa: BLE001, S110
        pass

    redis_ok = check_redis_health()
    dependencies = {"postgres": postgres_ok, "redis": redis_ok}

    if not postgres_ok or not redis_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready", "dependencies": dependencies}

    return {"status": "ready", "dependencies": dependencies}


@router.get("/metrics")
def metrics() -> Response:
    return Response(content=prometheus_text(), media_type="text/plain; version=0.0.4")
