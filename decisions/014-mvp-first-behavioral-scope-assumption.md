# ADR-014: MVP-First Behavioral Scope Assumption

**Date:** 2026-02-13
**Status:** Accepted

## Context

Behavioral Architecture now includes actors and use cases beyond the Heidi-only MVP (e.g., Learner, Payment Provider, Advertising Platform, Authentication Provider, Security Specialist). These future elements are necessary to preserve architectural flexibility and avoid costly restructuring later.

However, detailed design and implementation effort must prioritize immediate Heidi-only MVP delivery.

## Decision

Adopt an explicit modeling assumption:

- **Heidi-only MVP use cases and actor interactions are primary for near-term design decisions.**
- **Non-MVP elements are placeholders** used to preserve extension points and interface awareness.
- Placeholder future elements must not force premature implementation complexity into the MVP.
- Future elements may remain high-level until promoted into active scope.

## Rationale

- Preserves long-term architectural integrity while preventing near-term overengineering.
- Enables requirements and interfaces to evolve without massive refactoring.
- Keeps model complexity manageable by separating "must build now" from "must not forget later."

## Consequences

- Model reviews should prioritize correctness/completeness of MVP actor/use case paths first.
- Future elements are expected to be less detailed and may temporarily fail strict completeness heuristics until activated.
- Scope decisions should explicitly reclassify elements (e.g., future → mvp) when implementation planning begins.
