# ADR 1: Monorepo vs Polyrepo

## Context
We needed to decide whether to store the React frontend and FastAPI backend in a single repository (monorepo) or separate repositories (polyrepo).

## Decision
We decided to use a **Monorepo** (single repository) structure.

## Rationale
- Eases continuous integration (CI) since one PR can contain synchronized frontend and backend changes.
- Simplifies local development using a single Docker Compose file.
- Reduces cognitive load for a two-person team.

## Consequences
- Requires careful path filtering in GitHub Actions to only run frontend tests on frontend changes, and backend tests on backend changes.
