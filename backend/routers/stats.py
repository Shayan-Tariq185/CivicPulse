from collections import Counter
import json

from fastapi import APIRouter, Response

from redis_client import redis_db
from repositories import complaint_repo
from schemas.complaint import ComplaintCategory, ComplaintStatus
from schemas.stats import CategoryStat, StatsOut

router = APIRouter(prefix="/stats", tags=["statistics"])

@router.get("", response_model=StatsOut)
def get_stats(response: Response) -> StatsOut:
    CACHE_KEY = "civicpulse:stats"
    
    # 1. Try to get from Redis
    cached_stats = redis_db.get(CACHE_KEY)
    if cached_stats:
        response.headers["X-Cache"] = "HIT"
        return StatsOut.model_validate(json.loads(cached_stats))

    # 2. If MISS, calculate stats normally
    response.headers["X-Cache"] = "MISS"
    complaints = complaint_repo.list_all()
    
    # SQLAlchemy model returns strings, not Enums, so we just use the string directly
    status_counts = Counter(complaint.status for complaint in complaints)
    category_counts = Counter(complaint.category for complaint in complaints)

    stats = StatsOut(
        total=len(complaints),
        open=status_counts[ComplaintStatus.open.value],
        in_progress=status_counts[ComplaintStatus.in_progress.value],
        resolved=status_counts[ComplaintStatus.resolved.value],
        rejected=status_counts[ComplaintStatus.rejected.value],
        byCategory=[
            CategoryStat(
                category=category.value,
                count=category_counts[category.value],
            )
            for category in ComplaintCategory
        ],
    )
    
    # 3. Save to Redis for 15 seconds
    redis_db.setex(CACHE_KEY, 15, stats.model_dump_json())
    
    return stats
