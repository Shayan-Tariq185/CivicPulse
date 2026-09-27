from fastapi import APIRouter

from providers.history import recent_outcomes

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/providers")
def provider_outcomes() -> list[dict[str, object]]:
    return recent_outcomes()
