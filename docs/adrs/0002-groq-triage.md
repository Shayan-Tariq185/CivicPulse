# ADR 2: Choosing Groq for AI Triage

## Context
We needed an LLM provider to automatically triage complaints into specific categories (e.g., Roads, Utilities, Waste) based on the user's free-text description.

## Decision
We selected **Groq** (using Llama3 models) via their REST API instead of OpenAI, local huggingface models, or other providers.

## Rationale
- Groq's LPU architecture provides extremely low latency (often <200ms), which is critical for synchronous web requests so the user doesn't wait on the submit screen.
- It offers generous free tiers suitable for academic assignments.
- Easily integrates with standard Python HTTP clients and fallback patterns.

## Consequences
- Requires fallback logic (rules-based regex) in case of rate limits or network unavailability.
- Ties the triage implementation to external network dependencies.
