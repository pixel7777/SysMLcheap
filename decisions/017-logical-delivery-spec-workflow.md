# ADR-017: Logical Delivery Spec (LDS) Workflow Layer

**Date:** 2026-02-21
**Status:** Accepted

## Context

Our original MBSE→code flow was rigorous but felt too heavy for day-to-day iteration. We want to preserve detailed actor/use-case modeling while reducing overhead between behavioral architecture and implementation.

Specifically, we need a medium-granularity artifact that is:
- Structured enough for logical and physical architecture trade studies
- Concrete enough to generate code scaffolding and test cases
- Lightweight enough to maintain without full formal decomposition every cycle

## Decision

Introduce a **Logical Delivery Spec (LDS)** per use case as the default transition artifact between Behavioral and Physical/Implementation work.

Revised workflow:
1. Behavioral architecture (actors/use cases) remains the source of intent.
2. For each implementation-targeted use case, create/update an LDS file in `specs/use-cases/`.
3. Use LDS content to drive physical architecture trade decisions.
4. Generate implementation tasks, scaffolding, and acceptance tests from LDS.
5. Maintain traceability links from LDS to use case IDs, requirements IDs, and logical candidates.

## LDS Minimum Content

Each LDS must include:
- intent/outcome
- user stories
- business rules
- logical responsibilities (tech-agnostic)
- state/data concepts
- quality requirements
- acceptance tests (Given/When/Then)
- open tradeoff questions
- traceability references

## Rationale

- Keeps MBSE discipline where it gives the highest value (behavioral truth + traceability)
- Reduces modeling overhead before useful architecture and coding conversations
- Makes reviews easier in GitHub (single-file per use case, readable by non-modeling tools)
- Creates a stable bridge from intent to executable work items and tests

## Consequences

- Adds a new artifact type to govern and validate
- Requires rules to avoid LDS drift from behavioral/use-case sources
- Some deeply formal logical constructs may be deferred until needed
- Improves iteration speed while preserving architecture quality
