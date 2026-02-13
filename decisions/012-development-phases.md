# ADR-012: Development Phases

**Date:** 2026-02-13
**Status:** Accepted

## Context

The project spans from conceptual modeling to a deployed application. We need a phased approach that delivers value incrementally without over-planning.

## Decision

Six development phases:

1. **Phase 1: Tooling** (current) — metamodel, validation, diagram generation
2. **Phase 2: Behavioral & Logical Architecture** — model MVP use cases, activities, and future constraints
3. **Phase 3: Physical Architecture** — technology choices, versioning, configurations
4. **Phase 4: Work Management** — Kanban setup, model-driven task generation
5. **Phase 5: Dev Environment** — webapp (likely mobile-focused), deployment pipeline
6. **Phase 6: Iterative Development** — model → tasks → code → test → play → feedback

**Philosophy:** Model just ahead of code, not six months ahead.

## Rationale

- Each phase builds on the previous, with tangible output at each stage
- "Just ahead" modeling avoids analysis paralysis while maintaining architectural discipline
- Early phases (1-2) are low-cost and high-learning — discover problems before writing code
- Later phases can adapt based on what's learned in earlier ones

## Consequences

- Phase boundaries are guidelines, not gates — overlap is expected
- Must resist the temptation to model everything before building anything
- Phase 1 tooling quality directly impacts all subsequent phases
- Feedback from Phase 6 loops back to refine models (living architecture)
