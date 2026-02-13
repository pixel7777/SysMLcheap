# ADR-015: Logical Architecture Variant Management Policy

**Date:** 2026-02-13
**Status:** Accepted

## Context

The Language Questing System must support at least two major configurations over time:

- single-user MVP configuration (Heidi-focused)
- future multi-user/commercial configuration

In SysML-style modeling, these configurations can diverge in system context, system boundary details, interfaces, and logical composition. Our current YAML+PlantUML toolchain does not provide first-class product-line variability mechanisms (feature models, variant selections, 150% model filtering).

## Decision

Adopt the following variant management policy for logical architecture:

1. **Use separate context blocks per major configuration.**
2. **Use separate top-level system blocks per major configuration.**
3. **Allow shared reusable logical elements by reference/composition where appropriate.**
4. **Do not rely on block generalization/inheritance for variant decomposition in composition structures.**
   - If a common block exists, it is a documentation/reuse aid only.
   - It must not be used as the composed system-of-interest block in variant contexts.
5. **Use `status` tags for maturity/scope tracking, not as the primary variant mechanism.**

## Rationale

- Keeps each configuration boundary explicit and reviewable.
- Avoids conditional clutter in a single context/system model.
- Preserves freedom for physical architecture trades per variant.
- Aligns with practical team experience that block generalization in architecture composition is error-prone.

## Consequences

- Model size increases (multiple top-level context/system structures).
- Cross-variant consistency requires governance (naming, IDs, review checks).
- Shared elements remain possible without collapsing boundaries.
- Future variant expansion (e.g., enterprise/self-hosted) can follow the same pattern.
