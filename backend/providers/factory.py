from config import settings
from providers.base import TriageProvider
from providers.groq import GroqTriage
from providers.rules import RuleBasedTriage
from providers.simulated import SimulatedTriage


def get_triage_provider() -> TriageProvider:
    provider_name = settings.TRIAGE_PROVIDER.casefold()

    if provider_name == "rules":
        return RuleBasedTriage()

    if provider_name == "simulated":
        return SimulatedTriage()

    if provider_name == "groq":
        return GroqTriage(settings.GROQ_API_KEY, settings.GROQ_MODEL)

    raise RuntimeError(
        f"Unsupported TRIAGE_PROVIDER={settings.TRIAGE_PROVIDER!r}. "
        "Use groq, rules, or simulated."
    )
