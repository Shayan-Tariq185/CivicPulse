from collections import Counter

from fastapi import APIRouter

from repositories import complaint_repo
from schemas.complaint import ComplaintCategory, ComplaintStatus
from schemas.stats import CategoryStat, StatsOut

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("", response_model=StatsOut)
def get_stats() -> StatsOut:
    complaints = complaint_repo.list_all()
    status_counts = Counter(complaint.status.value for complaint in complaints)
    category_counts = Counter(complaint.category.value for complaint in complaints)

    return StatsOut(
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
