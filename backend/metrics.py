from __future__ import annotations

from collections import Counter
from threading import Lock


_lock = Lock()
_request_count = Counter()
_request_latency_ms: list[float] = []
_triage_latency_ms: list[float] = []
_fallback_count = 0


def record_request(method: str, path: str, status_code: int, latency_ms: float) -> None:
    with _lock:
        _request_count[(method, path, status_code)] += 1
        _request_latency_ms.append(latency_ms)


def record_triage(latency_ms: float, fallback: bool) -> None:
    global _fallback_count
    with _lock:
        _triage_latency_ms.append(latency_ms)
        if fallback:
            _fallback_count += 1


def _average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def prometheus_text() -> str:
    with _lock:
        lines = [
            "# HELP civicpulse_requests_total Total HTTP requests.",
            "# TYPE civicpulse_requests_total counter",
        ]
        for (method, path, status_code), count in sorted(_request_count.items()):
            lines.append(
                f'civicpulse_requests_total{{method="{method}",path="{path}",status="{status_code}"}} {count}'
            )

        lines.extend([
            "# HELP civicpulse_request_latency_ms_average Average request latency in milliseconds.",
            "# TYPE civicpulse_request_latency_ms_average gauge",
            f"civicpulse_request_latency_ms_average {_average(_request_latency_ms):.3f}",
            "# HELP civicpulse_triage_latency_ms_average Average triage latency in milliseconds.",
            "# TYPE civicpulse_triage_latency_ms_average gauge",
            f"civicpulse_triage_latency_ms_average {_average(_triage_latency_ms):.3f}",
            "# HELP civicpulse_triage_fallbacks_total Total triage fallbacks.",
            "# TYPE civicpulse_triage_fallbacks_total counter",
            f"civicpulse_triage_fallbacks_total {_fallback_count}",
        ])
        return "\n".join(lines) + "\n"
