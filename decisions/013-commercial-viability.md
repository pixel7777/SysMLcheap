# ADR-013: Commercial Viability Consideration

**Date:** 2026-02-13
**Status:** Accepted

## Context

The app starts as a personal project (Heidi learning Croatian) but has potential as a commercial product. Architecture decisions made now will either enable or constrain that evolution.

## Decision

- Physical architecture may have **multiple solutions per logical element** — some temporary, some scalable
- Distinguish between **prototype solutions** ("just for Heidi to test UX") and **commercial solutions** ("cost effective across a large user base")
- Architecture must **support evolution** from prototype to potential commercial offering
- **Lattix-type code dependency analysis** to be added later to manage architectural integrity

## Rationale

- Over-engineering for scale now wastes time on a product that may never launch commercially
- Under-engineering makes commercial pivot painful or impossible
- Dual-track thinking (prototype vs. commercial) keeps options open without over-investing
- Dependency analysis tools catch architectural erosion before it becomes technical debt

## Consequences

- Physical architecture documentation must capture both prototype and commercial variants
- Technology choices should favor options that scale (or can be swapped) without full rewrites
- Need periodic architecture reviews to assess commercial readiness
- Some throwaway work is acceptable and expected in early phases
