from typing import Protocol

from schemas.triage import TriageResult


class TriageProvider(Protocol):
    async def triage(self, text: str, location: str) -> TriageResult:
        """Classify a complaint and return validated triage data."""
