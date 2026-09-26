from pydantic import BaseModel


class CategoryStat(BaseModel):
    category: str
    count: int


class StatsOut(BaseModel):
    total: int
    open: int
    in_progress: int
    resolved: int
    rejected: int
    byCategory: list[CategoryStat]
