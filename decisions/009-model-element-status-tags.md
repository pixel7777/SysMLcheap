# ADR-009: Model Element Status Tags

**Date:** 2026-02-13
**Status:** Accepted

## Context

The YAML model contains elements at different maturity levels — some are needed for MVP, some are future features, some are commercial-only. We need a way to track scope and completeness per release.

## Decision

Elements in the YAML model get **status tags**:
- **MVP** — required for minimum viable product
- **Future** — planned but not for initial release
- **Commercial** — needed only for commercial/scaled deployment
- **Implemented** — development complete

The validator can check "are all MVP-tagged elements complete?" to assess release readiness.

## Rationale

- Supports incremental development without losing sight of the full vision
- Validator-driven status checks replace manual tracking
- Clear scope boundaries prevent feature creep in early phases
- Tags are lightweight (single field) and queryable

## Consequences

- Every model element needs a status field (schema change)
- Validator must support status-based filtering and reporting
- Team must agree on status assignments (governance)
- Status transitions need to be tracked (e.g., MVP → Implemented)
