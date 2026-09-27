from schemas.complaint import ComplaintCategory
from schemas.triage import Priority, TriageResult


_CATEGORY_RULES: tuple[tuple[tuple[str, ...], ComplaintCategory], ...] = (
    (("pipe", "leak", "water", "drain", "sewer"), ComplaintCategory.water),
    (("electricity", "electric", "power", "streetlight", "street light"), ComplaintCategory.electricity),
    (("garbage", "waste", "trash", "rubbish", "dump"), ComplaintCategory.waste),
    (("park", "playground", "swing", "recreation"), ComplaintCategory.parks),
    (("noise", "loud", "music", "construction"), ComplaintCategory.noise),
    (("crime", "unsafe", "attack", "theft", "security"), ComplaintCategory.safety),
    (("pothole", "road", "street", "traffic", "pavement"), ComplaintCategory.roads),
)

_HIGH_PRIORITY_TERMS = (
    "urgent",
    "emergency",
    "danger",
    "dangerous",
    "unsafe",
    "immediate",
    "critical",
)


class RuleBasedTriage:
    """Deterministic fallback provider that never calls an external service."""

    async def triage(self, text: str, location: str) -> TriageResult:
        normalized_text = f"{text} {location}".casefold()
        category = self._classify_category(normalized_text)
        priority = self._classify_priority(normalized_text)
        summary = self._build_summary(text, location)
        confidence = 0.9 if category is not ComplaintCategory.other else 0.55

        return TriageResult(
            category=category,
            priority=priority,
            summary=summary,
            confidence=confidence,
            triaged_by="rules",
        )

    @staticmethod
    def _classify_category(value: str) -> ComplaintCategory:
        for keywords, category in _CATEGORY_RULES:
            if any(keyword in value for keyword in keywords):
                return category
        return ComplaintCategory.other

    @staticmethod
    def _classify_priority(value: str) -> Priority:
        if any(term in value for term in _HIGH_PRIORITY_TERMS):
            return Priority.high
        return Priority.normal

    @staticmethod
    def _build_summary(text: str, location: str) -> str:
        source = " ".join(text.split()) or "Community issue reported."
        location_text = " ".join(location.split())
        summary = f"{source} Location: {location_text}." if location_text else source
        return summary[:137] + "..." if len(summary) > 140 else summary
