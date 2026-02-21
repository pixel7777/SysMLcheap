# ADR-018: Source-of-Truth Guardrails and Review Gates

**Date:** 2026-02-21
**Status:** Accepted

## Context

As the workflow evolved (Behavioral → LDS → Physical → Code → Views), we risked drift between artifacts and confusion about what Heidi should review.

We need:
- explicit authority hierarchy
- automated consistency checks
- a human-review checkpoint that does not require source-code review

## Decision

1. Adopt explicit source-of-truth hierarchy:
   - Behavioral truth: `model/behavioral.yaml`
   - Delivery truth: `specs/use-cases/*.lds.yaml`
   - Physical truth: `specs/physical/*.physical.md`
   - Implementation truth: code + tests
   - Views (`docs/index.html`, tables, demos): non-authoritative

2. Enforce guardrails via `tools/check_guardrails.py`:
   - LDS `useCaseRef` must map to behavioral use case IDs
   - Physical spec `Use Case Ref` must map to behavioral use case IDs
   - `docs/architecture/physical-index.md` must include refs present in LDS/physical artifacts

3. Add review gate:
   - Primary Heidi review checkpoint after physical intent updates is runnable demo behavior, not source-code inspection.

## Rationale

- Preserves MBSE traceability while reducing review burden
- Prevents silent drift between model, specs, and implementation
- Aligns workflow with stakeholder expertise and decision-making role

## Consequences

- Workflow now has explicit governance and validation burden (small, automated)
- PRs that change use-case artifacts should run guardrail checks
- Demo behavior is now first-class evidence for review completion
