# ADR 4: Vite and React for Frontend

## Context
We needed to build a responsive, single-page application (SPA) for the CivicPulse user interface.

## Decision
We selected **React** initialized with **Vite**, using **TypeScript**.

## Rationale
- React provides a robust component-based architecture for forms and dashboards.
- Vite offers significantly faster hot-module replacement (HMR) and build times compared to Create React App or Webpack.
- TypeScript enforces compile-time type safety, catching bugs early when mapping API responses to frontend models.

## Consequences
- Multi-stage Docker builds were necessary to serve the static Vite output using NGINX in production, reducing memory footprint compared to running the Vite dev server.
