from providers.rules import RuleBasedTriage
from schemas.triage import TriageResult


class SimulatedTriage:
    """Deterministic provider for local development and automated tests."""

    def __init__(self, *, should_fail: bool = False, malformed: bool = False) -> None:
        self.should_fail = should_fail
        self.malformed = malformed

    async def triage(self, text: str, location: str) -> TriageResult:
        if self.should_fail:
            raise TimeoutError("simulated provider timeout")

        if self.malformed:
            return TriageResult.model_validate({
                "category": "not-a-category",
                "priority": "not-a-priority",
                "summary": "invalid",
                "confidence": 2.0,
            })

        result = await RuleBasedTriage().triage(text, location)
        return result.model_copy(update={"triaged_by": "simulated"})
