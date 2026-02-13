# ADR-003: Three-Architecture Modeling Framework

**Date:** 2026-02-12
**Status:** Accepted

## Context

We need a structured approach to model the app at different levels of abstraction, from "what does it do" to "how is it built."

## Decision

Use a three-architecture framework with traceability between levels:
- **Behavioral Architecture** — Use cases, actors, and their relationships (what the system does from the user's perspective)
- **Logical Architecture** — System decomposition into functional blocks, interfaces, signals, and behaviors (how the system works conceptually)
- **Physical Architecture** — Concrete technology choices, deployment, databases, APIs (how it's actually built)

Each level "realizes" the one above: physical realizes logical, logical realizes behavioral.

## Rationale

- Standard MBSE practice (aligned with SAIC DE Style Guide process)
- Separates concerns: stakeholder needs vs. functional design vs. implementation
- Enables trade studies at the physical level without changing the logical architecture
- Traceability ensures nothing falls through the cracks
- Supports the commercial evolution path — same logical architecture, different physical solutions

## Consequences

- More upfront modeling work than jumping straight to code
- Requires discipline to maintain traceability as the model evolves
- Worth it for a project that may scale to a commercial offering
