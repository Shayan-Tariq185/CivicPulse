from collections import deque
from typing import TypedDict


class ProviderOutcome(TypedDict):
    provider: str
    latency_ms: int
    fallback: bool


_outcomes: deque[ProviderOutcome] = deque(maxlen=20)


def record_outcome(provider: str, latency_ms: int, fallback: bool) -> None:
    _outcomes.append({
        "provider": provider,
        "latency_ms": latency_ms,
        "fallback": fallback,
    })


def recent_outcomes() -> list[ProviderOutcome]:
    return list(_outcomes)
