import asyncio
from datetime import datetime, timezone

import pytest
from fastapi import Response

from metrics import prometheus_text
from providers.history import _outcomes, record_outcome, recent_outcomes
from providers.rules import RuleBasedTriage
from providers.simulated import SimulatedTriage
from routers import operations, stats
from schemas.complaint import ComplaintCreate, ComplaintCategory, ComplaintStatus, StatusUpdate
from schemas.triage import Priority, TriageResult
from services import complaint_service


class FakeRedis:
    def __init__(self, cached=None):
        self.cached = cached
        self.deleted = []
        self.setex_calls = []

    def get(self, _key):
        return self.cached

    def setex(self, key, ttl, value):
        self.setex_calls.append((key, ttl, value))

    def delete(self, key):
        self.deleted.append(key)


class FakeRecord:
    id = "CMP-TEST"
    title = "Test complaint"
    description = "A long enough test complaint description."
    category = ComplaintCategory.other.value
    status = ComplaintStatus.open.value
    location = "Test location"
    upvotes = 0
    submitted_at = datetime.now(timezone.utc)
    priority = Priority.normal.value
    ai_summary = "Test summary"
    triaged_by = "rules"
    triage_latency_ms = 1
    triage_confidence = 0.5


def test_short_title_is_rejected():
    with pytest.raises(ValueError):
        ComplaintCreate(title="x", description="A valid description", category="Other", location="Town")


def test_long_title_is_rejected():
    with pytest.raises(ValueError):
        ComplaintCreate(title="x" * 121, description="A valid description", category="Other", location="Town")


def test_invalid_category_is_rejected():
    with pytest.raises(ValueError):
        ComplaintCreate(title="Valid title", description="A valid description", category="invalid", location="Town")


def test_triage_summary_limit_is_enforced():
    with pytest.raises(ValueError):
        TriageResult(category=ComplaintCategory.other, priority=Priority.normal, summary="x" * 141, confidence=0.5)


def test_triage_confidence_bounds_are_enforced():
    with pytest.raises(ValueError):
        TriageResult(category=ComplaintCategory.other, priority=Priority.normal, summary="summary", confidence=1.1)


def test_rules_provider_classifies_water():
    result = asyncio.run(RuleBasedTriage().triage("Pipe leak near the road", "Sector 7"))
    assert result.category is ComplaintCategory.water


def test_rules_provider_marks_urgent_as_high():
    result = asyncio.run(RuleBasedTriage().triage("Urgent streetlight danger", "Main Road"))
    assert result.priority is Priority.high


def test_rules_provider_defaults_safely():
    result = asyncio.run(RuleBasedTriage().triage("Community issue", "Central Market"))
    assert result.category is ComplaintCategory.other
    assert result.priority is Priority.normal


def test_simulated_provider_is_deterministic():
    result = asyncio.run(SimulatedTriage().triage("Water pipe leak", "Block A"))
    assert result.triaged_by == "simulated"


def test_simulated_provider_can_fail():
    with pytest.raises(TimeoutError):
        asyncio.run(SimulatedTriage(should_fail=True).triage("Issue", "Block A"))


def test_provider_history_is_bounded_to_twenty():
    _outcomes.clear()
    for index in range(25):
        record_outcome(f"provider-{index}", index, False)
    assert len(recent_outcomes()) == 20
    assert recent_outcomes()[0]["provider"] == "provider-5"
    _outcomes.clear()


def test_stats_cache_miss_uses_thirty_second_ttl(monkeypatch):
    fake = FakeRedis()
    monkeypatch.setattr(stats, "redis_db", fake)
    monkeypatch.setattr(stats.complaint_repo, "list_all", lambda: [])
    response = Response()
    stats.get_stats(response)
    assert response.headers["X-Cache"] == "MISS"
    assert fake.setex_calls[0][1] == 30


def test_stats_cache_hit_uses_cached_value(monkeypatch):
    fake = FakeRedis('{"total":0,"open":0,"in_progress":0,"resolved":0,"rejected":0,"byCategory":[]}')
    monkeypatch.setattr(stats, "redis_db", fake)
    response = Response()
    result = stats.get_stats(response)
    assert response.headers["X-Cache"] == "HIT"
    assert result.total == 0
    assert fake.setex_calls == []


def test_create_invalidates_stats_cache(monkeypatch):
    fake = FakeRedis()
    provider_result = TriageResult(category=ComplaintCategory.other, priority=Priority.normal, summary="summary", confidence=0.5, triaged_by="rules")
    monkeypatch.setattr(complaint_service, "redis_db", fake)
    monkeypatch.setattr(complaint_service, "get_triage_provider", lambda: SimulatedProvider(provider_result))
    monkeypatch.setattr(complaint_service.complaint_repo, "create", lambda *args: FakeRecord())
    result = asyncio.run(complaint_service.create_complaint(ComplaintCreate(title="Valid title", description="A valid description", category="Other", location="Town")))
    assert result.id == "CMP-TEST"
    assert fake.deleted == ["civicpulse:stats"]


def test_update_status_invalidates_stats_cache(monkeypatch):
    fake = FakeRedis()
    updated = FakeRecord()
    updated.status = ComplaintStatus.in_progress.value
    monkeypatch.setattr(complaint_service, "redis_db", fake)
    monkeypatch.setattr(complaint_service.complaint_repo, "get_by_id", lambda _id: FakeRecord())
    monkeypatch.setattr(complaint_service.complaint_repo, "update_status", lambda *_args: updated)
    result = complaint_service.update_status("CMP-TEST", StatusUpdate(status=ComplaintStatus.in_progress))
    assert result.status is ComplaintStatus.in_progress
    assert fake.deleted == ["civicpulse:stats"]


def test_illegal_status_transition_returns_conflict(monkeypatch):
    monkeypatch.setattr(complaint_service.complaint_repo, "get_by_id", lambda _id: FakeRecord())
    with pytest.raises(Exception) as error:
        complaint_service.update_status("CMP-TEST", StatusUpdate(status=ComplaintStatus.resolved))
    assert getattr(error.value, "status_code", None) == 409


def test_missing_complaint_returns_not_found(monkeypatch):
    monkeypatch.setattr(complaint_service.complaint_repo, "get_by_id", lambda _id: None)
    with pytest.raises(Exception) as error:
        complaint_service.get_complaint("missing")
    assert getattr(error.value, "status_code", None) == 404


def test_health_does_not_require_dependencies():
    assert operations.health() == {"status": "ok"}


def test_ready_reports_healthy_dependencies(monkeypatch):
    class Connection:
        def __enter__(self):
            return self
        def __exit__(self, *_args):
            return False
        def execute(self, _query):
            return None

    class Engine:
        def connect(self):
            return Connection()

    monkeypatch.setattr(operations, "engine", Engine())
    monkeypatch.setattr(operations, "check_redis_health", lambda: True)
    response = Response()
    result = operations.ready(response)
    assert result["status"] == "ready"
    assert response.status_code == 200


def test_ready_reports_dependency_failure(monkeypatch):
    class Engine:
        def connect(self):
            raise RuntimeError("database down")

    monkeypatch.setattr(operations, "engine", Engine())
    monkeypatch.setattr(operations, "check_redis_health", lambda: False)
    response = Response()
    result = operations.ready(response)
    assert result["status"] == "not_ready"
    assert response.status_code == 503


def test_metrics_expose_request_and_triage_names():
    text = prometheus_text()
    assert "civicpulse_requests_total" in text
    assert "civicpulse_triage_fallbacks_total" in text


class SimulatedProvider:
    def __init__(self, result):
        self.result = result

    async def triage(self, _text, _location):
        return self.result
